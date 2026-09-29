"""Start the local web app. The prebuilt React frontend ships with the repository."""
import os
from pathlib import Path
from dotenv import load_dotenv
import uvicorn

if __name__ == '__main__':
    root = Path(__file__).resolve().parent
    load_dotenv(root / '.env')
    if not (root / 'backend/static/index.html').exists():
        raise SystemExit('Missing frontend build. Run: npm ci --prefix frontend && npm run build --prefix frontend')
    port = int(os.getenv('PORT', '8000'))
    print(f'\nOpen http://127.0.0.1:{port} in your browser. Press Ctrl+C here to stop.\n', flush=True)
    uvicorn.run('backend.main:app', host='127.0.0.1', port=port)
