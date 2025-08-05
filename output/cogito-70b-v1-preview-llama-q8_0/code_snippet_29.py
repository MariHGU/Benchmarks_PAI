from fastapi import FastAPI

app = FastAPI()

# For query string:
@app.post('/?user={user}')
def main(user: str):
    return {"user": user}

# Or for form data:
@app.post('/')
async def main(user: str = None):
    return {"user": user}