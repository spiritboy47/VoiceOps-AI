# ------main.py-----
from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from starlette.status import HTTP_302_FOUND

from app.routers import api
from app.auth import create_session, verify_session, authenticate

app = FastAPI(
    title="VoiceOps AI",
    description="VoiceOps AI Bot Dashboard API",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

# -----------------------------
# Helper: Check Login
# -----------------------------
def get_current_user(request: Request):
    session_cookie = request.cookies.get("session")
    if not session_cookie:
        return None
    return verify_session(session_cookie)


# -----------------------------
# Login Page
# -----------------------------
@app.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    if authenticate(username, password):
        session_token = create_session(username)
        response = RedirectResponse(url="/", status_code=HTTP_302_FOUND)
        response.set_cookie(
            key="session",
            value=session_token,
            httponly=True,
            max_age=1800  # 30 minutes
        )
        return response

    return templates.TemplateResponse(
        "login.html",
        {"request": request, "error": "Invalid credentials"}
    )


# -----------------------------
# Logout
# -----------------------------
@app.get("/logout")
def logout():
    response = RedirectResponse(url="/login", status_code=HTTP_302_FOUND)
    response.delete_cookie("session")
    return response


# -----------------------------
# Dashboard (Protected)
# -----------------------------
@app.get("/")
def dashboard(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=HTTP_302_FOUND)

    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "user": user["user"]}
    )


# -----------------------------
# Protect API Router
# -----------------------------
@app.middleware("http")
async def auth_middleware(request: Request, call_next):

    # Allow login and static files
    if request.url.path.startswith("/login") or request.url.path.startswith("/static"):
        return await call_next(request)

    # Protect API routes
    if request.url.path.startswith("/api"):
        session_cookie = request.cookies.get("session")
        if not session_cookie or not verify_session(session_cookie):
            return RedirectResponse(url="/login")

    return await call_next(request)


# Mount API
app.include_router(api.router, prefix="/api")


@app.get("/api")
def api_root():
    return {"message": "Welcome to VoiceOps AI API", "endpoints": ["/api/chat"]}