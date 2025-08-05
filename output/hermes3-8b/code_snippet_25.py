import requests

data = {'name': 'Smith'}
response = requests.post('http://127.0.0.1:8000/user', json=data)
print(response.json())