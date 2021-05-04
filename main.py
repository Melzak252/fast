import hashlib
from typing import Optional

from fastapi import FastAPI, Request, status, HTTPException, Cookie
from fastapi.responses import HTMLResponse, Response, JSONResponse
from pydantic import BaseModel
import datetime

app = FastAPI()
app.tokens = []
app.access_token = "AutoryzacjaUzyskana"
app.password = "NotSoSecurePa$$"
app.login = "4dm1n"


class User(BaseModel):
    user: Optional[str] = ""
    password: Optional[str] = ""


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
def login_session(*, user: str = None, password = None, response: Response):
    if password and user:
        if password == app.password and user == app.login:
            response.set_cookie(key="session_token", value=app.access_token)
            return JSONResponse(content={"messege": "Zalogowano"}, status_code=status.HTTP_201_CREATED)
        else:
            response.set_cookie(key="session_token", value="Nieautoryzowany")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    else:
        response.set_cookie(key="session_token", value="Nieautoryzowany")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@app.post("/login_token", status_code=status.HTTP_201_CREATED)
def login_session(*, user: str = None, password: str = None, response: Response):
    if password and user:
        if password == app.password and user == app.login:
            response.set_cookie(key="session_token", value=app.access_token)
            return JSONResponse(content={"token": app.access_token}, status_code=status.HTTP_201_CREATED)
        else:
            response.set_cookie(key="session_token", value="Nieautoryzowany")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    else:
        response.set_cookie(key="session_token", value="Nieautoryzowany")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

