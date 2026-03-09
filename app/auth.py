# ===========auth.py=========
from fastapi import Request, Form, HTTPException
from fastapi.responses import RedirectResponse
from itsdangerous import URLSafeSerializer
from app.config import SECRET_KEY, USERNAME, PASSWORD

serializer = URLSafeSerializer(SECRET_KEY)

def create_session(username: str):
    return serializer.dumps({"user": username})

def verify_session(session_cookie: str):
    try:
        return serializer.loads(session_cookie)
    except Exception:
        return None

def authenticate(username: str, password: str):
    return username == USERNAME and password == PASSWORD