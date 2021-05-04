import hashlib
from typing import Optional

from fastapi import FastAPI, Request, status, HTTPException, Cookie
from fastapi.responses import HTMLResponse, Response
from pydantic import BaseModel
import datetime

app = FastAPI()
app.tokens = []
app.access_token = "AutoryzacjaUzyskana"


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
def login(user: User, response: Response):

    if user.login and user.password:
        if user.login == "4dm1n" and user.password == "NotSoSecurePa$$":
            response.set_cookie(key="session_token", value=app.access_token)
            return {"message": "Zalogowano"}
        else:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED )

    else:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED )


@app.post("/login_token", status_code=status.HTTP_201_CREATED)
def login_token(user: User = None):
    if user:
        if user.login is None or user.password is None:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED)
        elif user.login == "4dm1n" and user.password == "NotSoSecurePa$$":
            return {"token": app.access_token}
        else:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED )
    else:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED )