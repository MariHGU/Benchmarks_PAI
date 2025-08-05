from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class UserRequest(BaseModel):
    user: str

@app.post('/')
def main(request: UserRequest):
    return {"user": request.user}