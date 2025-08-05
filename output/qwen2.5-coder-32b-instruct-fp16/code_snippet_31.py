import requests

url = 'http://127.0.0.1:8000'
data = {'username': 'Smith'}  # Match the field names in your Pydantic model
response = requests.post(url, json=data)
print(response.text)