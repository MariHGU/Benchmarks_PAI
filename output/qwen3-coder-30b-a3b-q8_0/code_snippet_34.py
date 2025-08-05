from fastapi import FastAPI, Body

app = FastAPI()

@app.post('/')
def main(user: str = Body(...)):
    return {"user": user}