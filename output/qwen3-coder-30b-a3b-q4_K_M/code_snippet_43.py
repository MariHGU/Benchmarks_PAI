from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class UserRequest(BaseModel):
    user: str

@app.post('/')
def main(user: UserRequest):
    return user

# For testing with your JavaScript code:
# The JavaScript should work as-is with the above code