from pydantic import BaseModel

class User(BaseModel):
    user: str

@app.post('/')
def main(user_data: User):
    return user_data.dict()