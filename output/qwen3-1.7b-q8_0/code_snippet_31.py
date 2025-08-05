import requests

url = "http://your-api-endpoint.com"
headers = {"Content-Type": "application/json"}
data = {"user": "smith"}
response = requests.post(url, json=data, headers=headers)