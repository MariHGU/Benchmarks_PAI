from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class UserData(BaseModel):
    user: str

@app.post('/')
def main(data: UserData):
    return data