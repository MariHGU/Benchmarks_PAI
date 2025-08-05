import requests

url = 'http://127.0.0.1:8000'
response = requests.post(f'{url}/?user=Smith')
print(response.text)