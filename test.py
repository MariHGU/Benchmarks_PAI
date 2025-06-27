import utils
from ollama import Client
import re, json, requests

api_key = utils.load_api_key()

client = Client(
    host="https://beta.chat.nhn.no/ollama",
    headers={
        'Authorization': 'Bearer ' + api_key,
    }
)

payload = {
    "model": "devstral:24b-small-2505-q4_K_M",
    "messages": [{"role": "user", "content": "Hva er værvarselet for i dag?"}],
    "stream": False,
}

headers = {
    "Authorization": "Bearer " + api_key,
    "Content-Type": "application/json",
}


r = requests.post(
    "https://beta.chat.nhn.no/ollama",
    headers=headers,
    data =json.dumps(payload),
    timeout=60,
)

r.raise_for_status()
raw_response = r.json()
print("DEBUG raw_response:\n", raw_response)

text_response = r
print("DEBUG text_response:\n", text_response)

# extract the content inside Message(...content="...") pattern
match = re.search(r"content=\"(.*?)\"", text_response)
if match:
    extracted = match.group(1)
    try:
        parsed = json.loads(extracted)
        print(parsed)
    except json.JSONDecodeError:
        raise ValueError(f"Model content was not JSON:\n{extracted}")
else:
    raise ValueError(f"Could not parse 'content' from response:\n{text_response}")