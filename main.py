from fastapi import FastAPI, Request, status, HTTPException
from fastapi.responses import  HTMLResponse
from pydantic import BaseModel
import datetime

app = FastAPI()
app.tokens = []


@app.get("/hello")
def root():
    html_response = f"<h1>Hello! Today day is {datetime.date.today()}</h1>"
    # return HTMLResponse(content=html_response, status_code=200)
    return html_response


