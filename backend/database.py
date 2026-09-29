"""Database: durable conversations, runs, stream events and file metadata."""
from datetime import datetime, timezone
from uuid import uuid4
from sqlalchemy import create_engine, Column, String, Text, Integer, Float, JSON, event, select
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from . import config


def uid(): return str(uuid4())
def now(): return datetime.now(timezone.utc).timestamp()

class Base(DeclarativeBase): pass

class Conversation(Base):
    __tablename__ = 'conversations'
    id = Column(String(36), primary_key=True, default=uid)
    owner = Column(String(36), nullable=False, index=True)
    title = Column(String(120), default='New conversation')
    created = Column(Float, default=now)
    active_run = Column(String(36), nullable=True)

class Message(Base):
    __tablename__ = 'messages'
    id = Column(String(36), primary_key=True, default=uid)
    conversation_id = Column(String(36), nullable=False, index=True)
    run_id = Column(String(36), nullable=False, index=True)
    role = Column(String(20), nullable=False)
    content = Column(Text, default='')
    status = Column(String(20), default='complete')
    created = Column(Float, default=now)

class Run(Base):
    __tablename__ = 'runs'
    id = Column(String(36), primary_key=True)
    conversation_id = Column(String(36), nullable=False, index=True)
    owner = Column(String(36), nullable=False)
    prompt = Column(Text, nullable=False)
    status = Column(String(20), default='queued')
    created = Column(Float, default=now)
    updated = Column(Float, default=now)

class StreamEvent(Base):
    __tablename__ = 'stream_events'
    id = Column(Integer, primary_key=True, autoincrement=True)
    run_id = Column(String(36), nullable=False, index=True)
    type = Column(String(40), nullable=False)
    payload = Column(JSON, nullable=False)

class Document(Base):
    __tablename__ = 'documents'
    id = Column(String(36), primary_key=True, default=uid)
    owner = Column(String(36), nullable=False, index=True)
    title = Column(String(160), nullable=False)
    object_key = Column(String(240), nullable=False)
    checksum = Column(String(64), nullable=False)
    size = Column(Integer, nullable=False)
    created = Column(Float, default=now)

class Artifact(Base):
    __tablename__ = 'artifacts'
    id = Column(String(36), primary_key=True, default=uid)
    owner = Column(String(36), nullable=False, index=True)
    conversation_id = Column(String(36), nullable=False, index=True)
    run_id = Column(String(36), nullable=False)
    title = Column(String(160), nullable=False)
    object_key = Column(String(240), nullable=False)
    size = Column(Integer, nullable=False)
    created = Column(Float, default=now)

engine = create_engine(config.DATABASE_URL, pool_pre_ping=True,
    connect_args={'check_same_thread': False, 'timeout': 30} if config.DATABASE_URL.startswith('sqlite') else {})
if config.DATABASE_URL.startswith('sqlite'):
    @event.listens_for(engine, 'connect')
    def sqlite_settings(dbapi, _):
        dbapi.execute('PRAGMA journal_mode=WAL')
        dbapi.execute('PRAGMA busy_timeout=30000')
Session = sessionmaker(engine, expire_on_commit=False)

def initialize(): Base.metadata.create_all(engine)

def emit(run_id: str, kind: str, payload: dict):
    with Session.begin() as db:
        db.add(StreamEvent(run_id=run_id, type=kind, payload=payload))
        run = db.get(Run, run_id)
        if run: run.updated = now()

def artifact_info(a):
    return {'id': a.id, 'title': a.title, 'size': a.size, 'run_id': a.run_id,
            'created': a.created, 'download_url': f'/api/artifacts/{a.id}/download'}

def events_after(run_id: str, after: int):
    with Session() as db:
        return [{'event_id': e.id, 'type': e.type, 'payload': e.payload, 'run_id': e.run_id}
            for e in db.scalars(select(StreamEvent).where(StreamEvent.run_id == run_id,
                StreamEvent.id > after).order_by(StreamEvent.id).limit(200))]
