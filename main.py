from fastapi import FastAPI, Request, status, HTTPException, Cookie
from fastapi.responses import HTMLResponse, Response
from pydantic import BaseModel
import datetime

app = FastAPI()
app.tokens = []
app.session_token = "AutoryzacjaUzyskana"


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
def login(user: str, password: str, response: Response):
    if user == "4dm1n" and password == "NotSoSecurePa$$":
        response.set_cookie(key="session_token", value=app.session_token)
        return {"message": "Zalogowano"}
    else:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)


@app.post("/login_token", status_code=201)
def login_token(*, response: Response, session_token: str = Cookie(None)):
    if session_token == app.session_token:
        return {"message": app.session_token}
    else:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Unauthorised")

