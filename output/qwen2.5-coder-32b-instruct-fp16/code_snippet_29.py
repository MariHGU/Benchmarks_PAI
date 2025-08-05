from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    username: str
    # Add other fields as necessary

@app.post('/')
def main(user: User):
    return user