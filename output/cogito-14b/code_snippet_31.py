from fastapi import FastAPI

app = FastAPI()

@app.post("/")
async def main(user: dict):
    return user  # This will parse the JSON body into a Python dictionary