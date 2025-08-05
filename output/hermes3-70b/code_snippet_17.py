import requests

url = 'http://127.0.0.1:8000'
data = {'user': 'Smith'}

response = requests.post(url, params=data)
print(response.text)