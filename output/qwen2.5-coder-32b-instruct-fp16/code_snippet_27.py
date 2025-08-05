from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class UserRequest(BaseModel):
    user: str

@app.post('/')
def main(user_request: UserRequest):
    return user_request.user