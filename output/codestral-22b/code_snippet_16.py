from fastapi import FastAPI
from pydantic import BaseModel

class User(BaseModel):
    user: str

app = FastAPI()

@app.post('/')
def main(user: User):
    return user.dict()