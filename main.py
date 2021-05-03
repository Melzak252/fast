import hashlib

from fastapi import FastAPI, Request, status, HTTPException, Cookie
from fastapi.responses import HTMLResponse, Response
from pydantic import BaseModel
import datetime

app = FastAPI()
app.tokens = []
app.secret_key = "AutoryzacjaUzyskana"
app.access_token = None


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


@app.post("/login_session", status_code=201)
def login(login: str, password: str, response: Response):
    print(login)
    print(password)
    if login and password:
        if login == "4dm1n" and password == "NotSoSecurePa$$":

            app.access_token = hashlib.sha256(f"{login}{password}{app.secret_key}".encode()).hexdigest()

            response.set_cookie(key="session_token", value=app.access_token)
            return {"message": "Zalogowano"}

    raise HTTPException(status.HTTP_401_UNAUTHORIZED, )


@app.post("/login_token", status_code=status.HTTP_201_CREATED)
def login_token(*, response: Response, session_token: str = Cookie("default")):

    if app.access_token and session_token:
        if session_token == app.access_token:
            return {"token": app.access_token}

    raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Unauthorised")
