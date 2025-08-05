import json
import requests

url = 'http://127.0.0.1:8000'
data = {'user': 'Smith'}
headers = {'Content-Type': 'application/json'}
response = requests.post(url, json=data, headers=headers)
print(response.text)