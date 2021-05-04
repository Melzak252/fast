import hashlib
from typing import Optional
import secrets
from fastapi import FastAPI, Request, status, HTTPException, Depends, Cookie
from fastapi.responses import HTMLResponse, Response, JSONResponse, PlainTextResponse, RedirectResponse
from pydantic import BaseModel
import datetime
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()
app.tokens = []
app.access_token = None
app.access_session = None
app.password = "NotSoSecurePa$$"
app.login = "4dm1n"
app.counter_session = 0
app.counter_token = 0

security = HTTPBasic()


class User(BaseModel):
    user: Optional[str] = None
    password: Optional[str] = None


def generate_html_response():
    html_content = f"""
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Hello! Today date is {datetime.date.today()}</h1>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


@app.get("/hello", response_class=HTMLResponse)
async def hello():
    return generate_html_response()


def check_auth(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, app.login)
    correct_password = secrets.compare_digest(credentials.password, app.password)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect login or password",
            headers={"WWW-Authenticate": "Basic"},
        )


@app.post("/login_session", status_code=status.HTTP_201_CREATED)
async def login_session(credentials: HTTPBasicCredentials = Depends(security), ):
    check_auth(credentials)
    response = Response(status_code=status.HTTP_201_CREATED)
    app.counter_session += 1
    app.access_session = hashlib.sha256(f"{app.login}{app.password}{app.counter_session}".encode()).hexdigest()
    response.set_cookie(key="session_token", value=app.access_session)
    return response


@app.post("/login_token", status_code=status.HTTP_201_CREATED)
async def login_token(credentials: HTTPBasicCredentials = Depends(security), ):
    check_auth(credentials)
    response = JSONResponse(content={"token": app.access_token}, status_code=status.HTTP_201_CREATED)
    app.counter_token += 1
    app.access_token = hashlib.sha256(f"{app.counter_token}{app.login}{app.password}".encode()).hexdigest()
    response.set_cookie(key="session_token", value=app.access_token)
    return response


@app.get("/welcome_session")
async def welcome_session(format: Optional[str] = None, session_token: Optional[str] = Cookie(None)):
    if not session_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect session token",
            headers={"WWW-Authenticate": "Basic"},
        )

    if session_token != app.access_session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect session token",
            headers={"WWW-Authenticate": "Basic"},
        )

    if format == "json":
        return JSONResponse(content={"message": "Welcome!"})
    elif format == "html":
        return HTMLResponse(content="<h1>Welcome!</h1>")
    else:
        return Response(content="Welcome!")

@app.get("/welcome_token")
async def welcome_token(format: Optional[str] = None, token: Optional[str] = None):
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect session token",
            headers={"WWW-Authenticate": "Basic"},
        )

    if token != app.access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect session token",
            headers={"WWW-Authenticate": "Basic"},
        )

    if format == "json":
        return JSONResponse(content={"message": "Welcome!"})
    elif format == "html":
        return HTMLResponse(content="<h1>Welcome!</h1>")
    else:
        return Response(content="Welcome!")


@app.delete("/logout_session", status_code=status.HTTP_302_FOUND)
async def logout_session(format: Optional[str] = None, session_token: Optional[str] = Cookie(None)):
    if not session_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect session token",
            headers={"WWW-Authenticate": "Basic"},
        )

    if session_token != app.access_session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session token is not correct",
            headers={"WWW-Authenticate": "Basic"},
        )

    return RedirectResponse(
        url=app.url_path_for(name="logged_out") + f"?format={format}",
        status_code=status.HTTP_302_FOUND
    )

@app.get("/logged_out", status_code=status.HTTP_200_OK)
async def logged_out(format: Optional[str] = None):
    if format == "json":
        return JSONResponse(content={"message": "Logged out!"}, status_code=status.HTTP_200_OK)
    elif format == "html":
        return HTMLResponse(content="<h1>Logged out!</h1>", status_code=status.HTTP_200_OK)
    else:
        return PlainTextResponse(content="Logged out!", status_code=status.HTTP_200_OK)
