from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class UserRequest(BaseModel):
    user: str

@app.post('/')
def main(user: UserRequest):
    return user.dict()

# For testing with curl:
# curl -X POST "http://localhost:8000/" -H "Content-Type: application/json" -d '{"user": "smith"}'