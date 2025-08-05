from fastapi import FastAPI
app = FastAPI()

@app.post('/')
def main(user):
    return user