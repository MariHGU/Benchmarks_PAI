import requests

url = 'http://127.0.0.1:8000'
data = {'user': 'Smith'}

# Using json parameter automatically sets the Content-Type header to application/json
response = requests.post(url, json=data)
print(response.text)