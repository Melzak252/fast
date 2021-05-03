from fastapi import FastAPI, Request, status, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import datetime

app = FastAPI()
app.tokens = []

def generate_html_response():
    html_content = f"""
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Hello! Today day is {datetime.date.today()}</h1>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/hello")
def root():
    return generate_html_response()


