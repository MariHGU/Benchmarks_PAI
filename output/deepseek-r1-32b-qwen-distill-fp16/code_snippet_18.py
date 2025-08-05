from fastapi import FastAPI, Request

app = FastAPI()

@app.post('/')
async def main(request: Request):
    data = await request.json()
    return data