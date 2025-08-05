from fastapi import FastAPI, Request
app = FastAPI()

@app.post('/')
async def main(request: Request):
    user = await request.json()
    return user