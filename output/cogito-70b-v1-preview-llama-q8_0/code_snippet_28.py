from fastapi import FastAPI

app = FastAPI()

@app.post('/')
async def main(data: dict):
    return {"user": data.get("user")}