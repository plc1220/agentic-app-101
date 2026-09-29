"""Configuration has local defaults; Compose supplies external service URLs."""
import os
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / '.env')
DATA = Path(os.getenv('DATA_DIR', str(ROOT / '.data'))).resolve()
DATA.mkdir(parents=True, exist_ok=True)
DATABASE_URL = os.getenv('DATABASE_URL', f'sqlite:///{DATA / "workshop.db"}')
REDIS_URL = os.getenv('REDIS_URL', '')
S3_ENDPOINT = os.getenv('S3_ENDPOINT', '')
S3_BUCKET = os.getenv('S3_BUCKET', 'workshop')
WORKER_URL = os.getenv('WORKER_URL', '')
WORKER_TOKEN = os.getenv('WORKER_TOKEN', '')
ROLE = os.getenv('SERVICE_ROLE', 'all')
MODE = os.getenv('AGENT_MODE', 'gemini')
MODEL = os.getenv('GEMINI_MODEL', 'gemini-3-flash-preview')
MAX_SECONDS = 180
MAX_STEPS = 30
MAX_OUTPUT = 60_000
MAX_UPLOAD = 1_000_000

def session_secret() -> str:
    if value := os.getenv('SESSION_SECRET'):
        return value
    path = DATA / 'session-secret'
    import secrets
    try:
        with path.open('x') as f:
            f.write(secrets.token_hex(32))
        path.chmod(0o600)
    except FileExistsError:
        pass
    return path.read_text().strip()
