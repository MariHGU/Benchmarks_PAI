from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Define a Pydantic model for the request body
class UserRequest(BaseModel):
    user: str

@app.post('/')
def main(user: UserRequest):  # Use the model as a type hint
    return user