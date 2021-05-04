import hashlib
from typing import Optional
import base64
from fastapi import FastAPI, Request, status, HTTPException, Cookie, Header
from fastapi.responses import HTMLResponse, Response, JSONResponse
from pydantic import BaseModel
import datetime

app = FastAPI()
app.tokens = []
app.access_token = "AutoryzacjaToken"
app.access_session = "AutoryzacjaSesja"
app.password = "NotSoSecurePa$$"
app.login = "4dm1n"

app.basicauth = base64.b64encode('4dm1n:NotSoSecuePa$$'.encode('ascii'))


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
def root():
    return generate_html_response()


@app.post("/login_session", status_code=status.HTTP_201_CREATED)
def login_session(*, user: str = None, password: str = None, request: Request):
    auth = request.headers["Authorisation"]
    if auth:
        if "Basic" in auth:
            auth = auth[6:]

        if auth == app.basicauth:
            response = JSONResponse(content={"token": app.access_token}, status_code=status.HTTP_201_CREATED)
            response.set_cookie(key="session_token", value=app.access_token)
            return response
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    elif user and password:
        if user == app.login and password == app.password:
            response = JSONResponse(content={"token": app.access_token}, status_code=status.HTTP_201_CREATED)
            response.set_cookie(key="session_token", value=app.access_token)
            return response
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@app.post("/login_token", status_code=status.HTTP_201_CREATED)
def login_session(*, user: str = None, password: str = None, request: Request):
    auth = request.headers["Authorisation"]
    if auth:
        if "Basic" in auth:
            auth = auth[6:]

        if auth == app.basicauth:
            response = JSONResponse(content={"token": app.access_token}, status_code=status.HTTP_201_CREATED)
            response.set_cookie(key="session_token", value=app.access_token)
            return response
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    elif user and password:
        if user == app.login and password == app.password:
            response = JSONResponse(content={"token": app.access_token}, status_code=status.HTTP_201_CREATED)
            response.set_cookie(key="session_token", value=app.access_token)
            return response
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
