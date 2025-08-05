import requests
headers = {'Content-Type': 'application/json'}
url = 'http://127.0.0.1:8000'
data = json.dumps({"user": "Smith"})
response = requests.post(url, headers=headers, data=data)
print(response.text)