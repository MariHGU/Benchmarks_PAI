import os, json, requests, asyncio
from deepeval.models import DeepEvalBaseLLM, OllamaModel
from ollama import Client, AsyncClient
from ollama import ChatResponse

def load_api_key(path: str = ".api_key.txt") -> str:
    with open(path, "r") as f:
        return f.read().strip()

# def call_llm_api(client, prompt):
#     chat = client.chat(model='gemma3n:e4b-it-q8_0', messages=[{
#         'role': 'user',
#         'content': prompt,
#     }])
#     # Isolate the json response
#     # if hasattr(chat, 'message') and hasattr(chat.message, 'content'):
#     #     chat = chat.message.content
#     # else:
#     #     print("Failed to parse message content")
#     #     return None
#     print("Chat response:", chat)
#     return chat

class OllamaLocalModel(OllamaModel):
    def __init__(
            self, 
            model: str = "gemma3n:e4b-it-q8_0", 
            base_url: str = "https://beta.chat.nhn.no/ollama",
            api_key_file: str = ".api_key.txt"):
        super().__init__(model=model, base_url=base_url)
        self.api_key_file = api_key_file
        # self.api_key = load_api_key(api_key_file)
        self.client = Client(host=self.base_url)

    def load_model(self,  async_mode: bool = False):
        api_key = self.get_api_key()
        if not async_mode:
            return  Client(
                host="https://beta.chat.nhn.no/ollama",
                headers={
                    'Authorization': 'Bearer ' + api_key,
                }
            )
        else:
            return AsyncClient(
                host="https://beta.chat.nhn.no/ollama",
                headers={
                    'Authorization': 'Bearer ' + api_key,
                }
            )
        
    def get_api_key(self):
        return load_api_key()
    