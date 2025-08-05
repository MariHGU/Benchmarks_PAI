from fastapi import FastAPI, Form

app = FastAPI()

@app.post('/')
def main(user: str):
    return {"user": user}