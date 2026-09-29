"""Object storage, a separate workspace filesystem, and a TTL cache."""
import hashlib
import json
import threading
import time
from pathlib import Path
from . import config

class ObjectStore:
    def __init__(self):
        self.local = config.DATA / 'objects'
        self.local.mkdir(exist_ok=True)
        self.client = None
        if config.S3_ENDPOINT:
            import boto3
            from botocore.config import Config
            self.client = boto3.client('s3', endpoint_url=config.S3_ENDPOINT,
                region_name='us-east-1', config=Config(s3={'addressing_style': 'path'}))
    def initialize(self):
        if self.client:
            from botocore.exceptions import ClientError
            try: self.client.head_bucket(Bucket=config.S3_BUCKET)
            except ClientError as exc:
                if str(exc.response['Error']['Code']) not in ('404', 'NoSuchBucket'): raise
                try: self.client.create_bucket(Bucket=config.S3_BUCKET)
                except ClientError as inner:
                    if inner.response['Error']['Code'] not in ('BucketAlreadyOwnedByYou', 'BucketAlreadyExists'): raise
    def path(self, key):
        path = (self.local / key).resolve()
        if self.local.resolve() not in path.parents: raise ValueError('Invalid object key')
        return path
    def put(self, key: str, data: bytes):
        if self.client:
            self.client.put_object(Bucket=config.S3_BUCKET, Key=key, Body=data,
                ContentType='text/markdown; charset=utf-8')
        else:
            path = self.path(key)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
    def get(self, key: str) -> bytes:
        if self.client:
            return self.client.get_object(Bucket=config.S3_BUCKET, Key=key)['Body'].read()
        return self.path(key).read_bytes()

class Cache:
    def __init__(self):
        self.items = {}
        self.lock = threading.Lock()
        self.client = None
        if config.REDIS_URL:
            import redis
            self.client = redis.Redis.from_url(config.REDIS_URL, decode_responses=True,
                socket_connect_timeout=2, socket_timeout=2)
    def get(self, key):
        if self.client:
            try: return self.client.get(key)
            except Exception: return None  # Cache failure must not lose the authoritative data.
        with self.lock:
            value = self.items.get(key)
            if value and value[0] > time.monotonic(): return value[1]
            self.items.pop(key, None)
    def put(self, key, value):
        if self.client:
            try: self.client.setex(key, 300, value)
            except Exception: pass
        else:
            with self.lock:
                if len(self.items) >= 128: self.items.pop(next(iter(self.items)))
                self.items[key] = (time.monotonic() + 300, value)

objects = ObjectStore()
cache = Cache()

def digest(data): return hashlib.sha256(data).hexdigest()

def stage_report(run_id: str, artifact_id: str, content: str) -> bytes:
    # IDs come from the application, not model-supplied paths.
    folder = config.DATA / 'workspaces' / run_id
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f'{artifact_id}.md'
    path.write_text(content, encoding='utf-8')
    return path.read_bytes()
