from fastapi import FastAPI, Body
from typing import Optional

app = FastAPI()

@app.post('/')
def main(user: Optional[str] = Body(None)):
    return {"user": user}