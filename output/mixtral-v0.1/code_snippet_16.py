from fastapi import FastAPI;
app = FastAPI();

@app.post('/')
def main(user: str):
    return {"user": user}