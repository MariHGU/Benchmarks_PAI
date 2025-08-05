from fastapi import FastAPI

app = FastAPI()

@app.post('/')
def main(user_data: dict):
    return user_data