from fastapi import FastAPI
from typing import Dict

app = FastAPI()

@app.post('/')
def main(user: Dict[str, str]):
    return user