from pydantic import BaseModel

class UserData(BaseModel):
    user: str