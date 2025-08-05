from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    user: str

@app.post('/')
def main(user: User):
    return user.dict()