from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class UserInput(BaseModel):
    user: str  # This specifies that 'user' is a string field

@app.post('/')
def main(user_input: UserInput):
    return user_input.dict()  # Return the data as a dictionary