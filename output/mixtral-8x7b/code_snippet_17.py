import requests
url = 'http://127.0.0.1:8000'
data = {'user': 'Smith'}
headers = {'Content-Type': 'application/json'} # This line is added
response = requests.post(url, json=data, headers=headers) # This line is modified
print(response.text)