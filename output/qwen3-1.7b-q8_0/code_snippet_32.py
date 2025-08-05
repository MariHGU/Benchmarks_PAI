from fastapi import FastAPI
import json
import requests

app = FastAPI()

@app.post("/submit")
def submit_user(username: str):
    return {"message": f"User {username} submitted successfully."}

# Example request
url = "http://your-api-endpoint.com/submit"
headers = {"Content-Type": "application/json"}
data = {"user": "smith"}
response = requests.post(url, json=data, headers=headers)
print(response.status_code)
print(response.json())