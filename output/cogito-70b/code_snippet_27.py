from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    user: str

@app.post('/')
def main(user_data: User):
    return {"received_user": user_data.user}