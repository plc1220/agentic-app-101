"""FastAPI API. Local mode hosts React and the worker; Compose separates them."""
import asyncio
import hmac
import json
import re
from contextlib import asynccontextmanager
from pathlib import Path
from uuid import UUID
from urllib.parse import urlparse
import httpx
from fastapi import FastAPI, Request, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse, StreamingResponse, Response, FileResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.trustedhost import TrustedHostMiddleware
from itsdangerous import URLSafeSerializer, BadSignature
from pydantic import BaseModel, Field
from sqlalchemy import select, update
from . import config, agent
from .database import (Session, initialize, Conversation, Message, Run, StreamEvent,
    Document, Artifact, now, uid, emit, events_after, artifact_info, engine)
from .storage import objects, digest


def fail_dispatch(run_id, message):
    with Session.begin() as db:
        run = db.get(Run, run_id)
        if not run or run.status != 'queued': return
        run.status, run.updated = 'failed', now()
        db.execute(update(Conversation).where(Conversation.active_run == run_id).values(active_run=None))
        db.execute(update(Message).where(Message.run_id == run_id, Message.role == 'assistant').values(status='failed'))
    emit(run_id, 'run.failed', {'error': message})


async def dispatch(run_id):
    if config.WORKER_URL:
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                response = await client.post(config.WORKER_URL + f'/internal/runs/{run_id}',
                    headers={'Authorization': 'Bearer ' + config.WORKER_TOKEN})
                response.raise_for_status()
        except Exception:
            fail_dispatch(run_id, 'The agent service is unavailable. Start it and try again.')
    else:
        agent.launch(run_id)


async def cancellation_watch():
    while True:
        await asyncio.sleep(.3)
        with Session() as db:
            cancelled = list(db.scalars(select(Run.id).where(Run.status == 'cancelling')))
        for run_id in cancelled:
            await agent.cancel_task(run_id)


@asynccontextmanager
async def lifespan(app):
    if config.MODE not in ('gemini', 'sample'): raise RuntimeError('AGENT_MODE must be gemini or sample')
    if config.ROLE == 'agent':
        if not config.WORKER_TOKEN: raise RuntimeError('Agent service requires WORKER_TOKEN')
        # API owns schema creation and sample ingestion in the multi-container version.
        for attempt in range(60):
            try:
                with Session() as db: db.execute(select(Conversation.id).limit(1))
                break
            except Exception:
                if attempt == 59: raise
                await asyncio.sleep(1)
    else:
        initialize()
        objects.initialize()
        for path in sorted((config.ROOT / 'sample-documents').glob('*.md')):
            document_id = 'sample-' + path.stem
            body = path.read_bytes()
            key = 'samples/' + path.name
            objects.put(key, body)
            with Session.begin() as db:
                doc = db.get(Document, document_id)
                if not doc:
                    doc = Document(id=document_id, owner='sample')
                    db.add(doc)
                doc.title, doc.object_key, doc.checksum, doc.size = path.stem.title() + ' region report', key, digest(body), len(body)
    if config.ROLE in ('all', 'agent'):
        with Session.begin() as db:
            unfinished = list(db.scalars(select(Run).where(Run.status.in_(['queued','running','cancelling']))))
            for run in unfinished:
                run.status = 'failed'
                db.execute(update(Message).where(Message.run_id == run.id, Message.role == 'assistant').values(status='failed'))
                db.execute(update(Conversation).where(Conversation.active_run == run.id).values(active_run=None))
                db.add(StreamEvent(run_id=run.id, type='run.failed', payload={'error':'Agent service restarted. Partial output was saved; submit again to retry.'}))
        watcher = asyncio.create_task(cancellation_watch())
    else: watcher = None
    yield
    if watcher: watcher.cancel()
    for task in list(agent.TASKS.values()): task.cancel()
    if agent.TASKS: await asyncio.gather(*list(agent.TASKS.values()), return_exceptions=True)
    engine.dispose()

app = FastAPI(title='Agentic App 101', lifespan=lifespan)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=__import__('os').getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1,api,agent').split(','))
signer = URLSafeSerializer(config.session_secret(), salt='workshop-browser')

@app.middleware('http')
async def session_and_origin(request: Request, call_next):
    # Worker has no browser-facing endpoints and must never be published by Compose.
    if config.ROLE == 'agent' and not (request.url.path.startswith('/internal/') or request.url.path == '/health'):
        return JSONResponse({'detail':'Not found'}, status_code=404)
    internal = request.url.path.startswith('/internal/')
    if internal:
        expected = 'Bearer ' + config.WORKER_TOKEN
        if config.ROLE not in ('agent', 'all') or not config.WORKER_TOKEN or not hmac.compare_digest(request.headers.get('authorization', ''), expected):
            return JSONResponse({'detail':'Unauthorized'}, status_code=401)
    elif request.url.path.startswith('/api/') and request.method not in ('GET','HEAD','OPTIONS'):
        origin = request.headers.get('origin')
        host = request.headers.get('host', '')
        allowed = set(__import__('os').getenv('ALLOWED_ORIGINS','http://127.0.0.1:5173,http://localhost:5173').split(','))
        if (origin and urlparse(origin).netloc != host and origin not in allowed) or request.headers.get('x-requested-with') != 'workshop':
            return JSONResponse({'detail':'Use the workshop application on the same origin.'}, status_code=403)
    fresh = False
    try:
        owner = signer.loads(request.cookies.get('workshop_session', ''))
        UUID(owner)
    except (BadSignature, ValueError, TypeError):
        owner, fresh = uid(), True
    request.state.owner = owner
    response = await call_next(request)
    if fresh and not internal:
        response.set_cookie('workshop_session', signer.dumps(owner), httponly=True,
            samesite='strict', secure=request.url.scheme == 'https', max_age=60*60*24*30)
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Referrer-Policy'] = 'same-origin'
    return response


def owned(db, model, item_id, owner):
    item = db.get(model, item_id)
    if not item or item.owner != owner: raise HTTPException(404, 'Not found')
    return item

def document_info(d):
    return {'id':d.id,'title':d.title,'size':d.size,'sample':d.owner == 'sample',
            'download_url':f'/api/documents/{d.id}/download'}

@app.get('/health')
def health(): return {'status':'ok', 'role':config.ROLE}

@app.get('/api/bootstrap')
def bootstrap(request: Request):
    key = __import__('os').getenv('GEMINI_API_KEY', '').strip()
    with Session() as db:
        conversations = list(db.scalars(select(Conversation).where(Conversation.owner == request.state.owner).order_by(Conversation.created.desc())))
        documents = list(db.scalars(select(Document).where(Document.owner.in_(['sample',request.state.owner])).order_by(Document.created)))
    return {'mode':config.MODE,'model':config.MODEL,'configured':bool(key and key != 'paste_your_key_here') or config.MODE == 'sample',
        'stack':{'frontend':'React + TypeScript','api':'FastAPI','agent':'Deep Agents + Gemini' if config.MODE == 'gemini' else 'Scripted sample (no model)',
                 'database':'SQLite' if config.DATABASE_URL.startswith('sqlite') else 'PostgreSQL',
                 'cache':'Redis' if config.REDIS_URL else 'In-memory TTL cache',
                 'objects':'MinIO / S3' if config.S3_ENDPOINT else 'Local object store','files':'Run workspace'},
        'conversations':[{'id':c.id,'title':c.title,'created':c.created} for c in conversations],
        'documents':[document_info(d) for d in documents]}

@app.post('/api/conversations')
def create_conversation(request: Request):
    with Session.begin() as db:
        c = Conversation(id=uid(), owner=request.state.owner)
        db.add(c)
        db.flush()
        return {'id':c.id, 'title':c.title, 'created':c.created}

@app.get('/api/conversations/{conversation_id}')
def get_conversation(conversation_id: str, request: Request):
    with Session() as db:
        c = owned(db, Conversation, conversation_id, request.state.owner)
        messages = list(db.scalars(select(Message).where(Message.conversation_id == c.id).order_by(Message.created)))
        artifacts = list(db.scalars(select(Artifact).where(Artifact.conversation_id == c.id).order_by(Artifact.created)))
        runs = list(db.scalars(select(Run).where(Run.conversation_id == c.id).order_by(Run.created)))
        return {'id':c.id, 'title':c.title, 'active_run':c.active_run,
            'messages':[{'id':m.id,'run_id':m.run_id,'role':m.role,'content':m.content,'status':m.status} for m in messages],
            'artifacts':[artifact_info(a) for a in artifacts],
            'runs':[{'id':r.id,'status':r.status} for r in runs]}

class RunInput(BaseModel):
    prompt: str = Field(min_length=1, max_length=8000)
    request_id: UUID

@app.post('/api/conversations/{conversation_id}/runs')
async def start_run(conversation_id: str, body: RunInput, request: Request):
    prompt = body.prompt.strip()
    if not prompt: raise HTTPException(422, 'Enter a message')
    run_id = str(body.request_id)
    with Session.begin() as db:
        c = owned(db, Conversation, conversation_id, request.state.owner)
        existing = db.get(Run, run_id)
        if existing:
            if existing.owner != request.state.owner or existing.conversation_id != c.id or existing.prompt != prompt:
                raise HTTPException(409, 'Request ID already used')
            return {'run_id':run_id, 'status':existing.status}
        claim = db.execute(update(Conversation).where(Conversation.id == c.id, Conversation.active_run.is_(None)).values(active_run=run_id))
        if not claim.rowcount: raise HTTPException(409, 'Wait for this conversation’s active run or stop it first.')
        if c.title == 'New conversation': c.title = prompt[:70]
        db.add(Run(id=run_id, conversation_id=c.id, owner=request.state.owner, prompt=prompt))
        db.add(Message(id=uid(), conversation_id=c.id, run_id=run_id, role='user', content=prompt, created=now()))
        db.add(Message(id=uid(), conversation_id=c.id, run_id=run_id, role='assistant', content='', status='streaming', created=now()+.001))
    await dispatch(run_id)
    return {'run_id':run_id, 'status':'queued'}

@app.get('/api/runs/{run_id}/events')
async def stream_events(run_id: str, request: Request, after: int = 0):
    with Session() as db: owned(db, Run, run_id, request.state.owner)
    try: after = max(0, after, int(request.headers.get('last-event-id', '0')))
    except ValueError: raise HTTPException(400, 'Invalid event ID')
    async def events():
        cursor, idle = after, 0
        while not await request.is_disconnected():
            batch = events_after(run_id, cursor)
            for item in batch:
                cursor = item['event_id']
                yield f'id: {cursor}\ndata: {json.dumps(item)}\n\n'
                if item['type'] in ('run.completed','run.failed','run.cancelled'): return
            if not batch:
                with Session() as db:
                    run = db.get(Run, run_id)
                    status, updated = run.status, run.updated
                # Terminal event insertion follows the status commit; allow a short grace period.
                if status in agent.TERMINAL and now() - updated > 2:
                    yield f'data: {json.dumps({"type":"run."+status,"payload":{},"run_id":run_id})}\n\n'
                    return
                idle += 1
                if idle % 40 == 0: yield ': heartbeat\n\n'
                await asyncio.sleep(.25)
    return StreamingResponse(events(), media_type='text/event-stream',
        headers={'Cache-Control':'no-cache, no-transform','X-Accel-Buffering':'no'})

@app.post('/api/runs/{run_id}/cancel')
async def cancel(run_id: str, request: Request):
    with Session.begin() as db:
        run = owned(db, Run, run_id, request.state.owner)
        if run.status in agent.TERMINAL: return {'status':run.status}
        if run.status == 'queued':
            run.status, run.updated = 'cancelled', now()
            db.execute(update(Conversation).where(Conversation.active_run == run_id).values(active_run=None))
            db.execute(update(Message).where(Message.run_id == run_id, Message.role == 'assistant').values(status='cancelled'))
            db.add(StreamEvent(run_id=run_id, type='run.cancelled', payload={}))
            return {'status':'cancelled'}
        run.status = 'cancelling'
    if config.WORKER_URL:
        try:
            async with httpx.AsyncClient(timeout=3) as client:
                await client.post(config.WORKER_URL + f'/internal/runs/{run_id}/cancel',
                    headers={'Authorization':'Bearer '+config.WORKER_TOKEN})
        except Exception: pass  # Agent also checks the persisted cancellation flag.
    else: await agent.cancel_task(run_id)
    return {'status':'cancelling'}

@app.post('/internal/runs/{run_id}')
async def internal_run(run_id: str):
    with Session() as db:
        if not db.get(Run, run_id): raise HTTPException(404, 'Unknown run')
    agent.launch(run_id)
    return {'accepted':True}

@app.post('/internal/runs/{run_id}/cancel')
async def internal_cancel(run_id: str):
    await agent.cancel_task(run_id)
    return {'accepted':True}

@app.post('/api/documents')
async def upload(request: Request, file: UploadFile = File(...)):
    name = Path((file.filename or '').replace('\\','/')).name
    if Path(name).suffix.lower() not in ('.txt','.md'): raise HTTPException(415, 'Upload a .txt or .md document.')
    content = await file.read(config.MAX_UPLOAD+1)
    await file.close()
    if len(content) > config.MAX_UPLOAD: raise HTTPException(413, 'Maximum file size is 1 MB.')
    try: text = content.decode('utf-8')
    except UnicodeDecodeError: raise HTTPException(415, 'Use a UTF-8 text file.')
    if not text.strip() or '\x00' in text: raise HTTPException(422, 'Upload a non-empty text document.')
    document_id = uid()
    key = f'uploads/{request.state.owner}/{document_id}.txt'
    objects.put(key, content)
    with Session.begin() as db:
        doc = Document(id=document_id, owner=request.state.owner, title=name[:160], object_key=key, checksum=digest(content), size=len(content))
        db.add(doc)
        db.flush()
        return document_info(doc)

@app.get('/api/documents/{document_id}/download')
def download_document(document_id: str, request: Request):
    with Session() as db:
        doc = db.get(Document, document_id)
        if not doc or doc.owner not in ('sample',request.state.owner): raise HTTPException(404, 'Not found')
        content = objects.get(doc.object_key)
    return Response(content, media_type='text/plain', headers={'Content-Disposition':'inline'})

@app.get('/api/artifacts/{artifact_id}')
def get_artifact(artifact_id: str, request: Request):
    with Session() as db:
        artifact = owned(db, Artifact, artifact_id, request.state.owner)
        return {**artifact_info(artifact), 'content':objects.get(artifact.object_key).decode('utf-8')}

@app.get('/api/artifacts/{artifact_id}/download')
def download_artifact(artifact_id: str, request: Request):
    with Session() as db:
        artifact = owned(db, Artifact, artifact_id, request.state.owner)
        content = objects.get(artifact.object_key)
    return Response(content, media_type='text/markdown', headers={'Content-Disposition':f'attachment; filename="briefing-{artifact_id}.md"'})

static = config.ROOT / 'backend/static'
if static.exists():
    app.mount('/assets', StaticFiles(directory=static/'assets'), name='assets')
    @app.get('/')
    def index(): return FileResponse(static/'index.html')
