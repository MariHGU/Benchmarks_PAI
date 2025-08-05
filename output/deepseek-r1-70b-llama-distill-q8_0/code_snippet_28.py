from fastapi import FastAPI, Body

app = FastAPI()

@app.post('/')
def main(user: str = Body(...)):  # The '...' ensures it's a required parameter
    return {'user': user}