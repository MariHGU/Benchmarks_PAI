import json, logging, os, requests
from deepeval.models import DeepEvalBaseLLM, OllamaModel
from ollama import Client, AsyncClient
from ollama import ChatResponse
from groq import Groq, AsyncGroq


def load_api_key(path: str = ".api_key.txt") -> str:
    """
    Load the API key from a specified file.
    
    Args:
        path (str): The file path to the API key. Defaults to ".api_key.txt".
    Returns:
        str: The API key read from the file.
    """
    with open(path, "r") as f:
        return f.read().strip()

class OllamaLocalModel(OllamaModel):
    """
    A class to interact with Ollama's local models.
    This class extends OllamaModel to provide methods for generating text
    using Ollama's API with an API key for authentication.
    
    Attributes:
        model (str): The name of the Ollama model to use.
        base_url (str): The base URL for the Ollama API.
        api_key_file (str): The file path to the API key.
    """
    def __init__(
            self, 
            model: str = "gemma3n:e4b-it-q8_0", 
            base_url: str = "https://beta.chat.nhn.no/ollama",
            api_key_file: str = ".api_key.txt"):
        super().__init__(model=model, base_url=base_url)
        self.api_key_file = api_key_file
        self.client = Client(host=self.base_url)

    def load_model(self,  async_mode: bool = False) -> Client:
        api_key = self.get_api_key()
        if not async_mode:
            return  Client(
                host=self.base_url,
                headers={
                    'Authorization': 'Bearer ' + api_key,
                }
            )
        else:
            return AsyncClient(
                host=self.base_url,
                headers={
                    'Authorization': 'Bearer ' + api_key,
                }
            )
        
    def get_api_key(self) -> str:
        return load_api_key()
    

class GroqModel(DeepEvalBaseLLM):
    """A class to interact with Groq's LLMs.
    This class extends DeepEvalBaseLLM to provide methods for generating text
    using Groq's API.
    
    Attributes:
        model_name (str): The name of the Groq model to use.
    
    """
    def __init__(self, model_name: str = "llama-3.3-70b-versatile", async_mode: bool = False):
        super().__init__(model_name=model_name)

    def load_model(self, async_mode: bool = False) -> Groq:
        api_key = load_api_key(path=".groq_api_key.txt")
        if not async_mode:
            return Groq(api_key = api_key)
        else:
            return AsyncGroq(api_key = api_key)
        
    def generate(self, prompt: str) -> str:
        groq_client = self.load_model(async_mode=False)
        response = groq_client.chat.completions.create(
            messages=[
                {"role": "user", 
                 "content": prompt}
            ],
            model=self.model_name,
        )
        return response.choices[0].message.content
    
    async def a_generate(self, prompt: str) -> str:
        groq_client = self.load_model(async_mode=True)
        response = await groq_client.chat.completions.create(
            messages=[
                {"role": "user", 
                "content": prompt}
            ],
            model=self.model_name,
        )
        return response.choices[0].message.content
    
    def get_model_name(self) -> str:
        return self.model_name



class CustomRelativeFormatter(logging.Formatter):
    """
    ChatGPT-4o generated code:
    A custom logging formatter that formats the time of the log record
    """
    
    def formatTime(self, record, datefmt=None):
        # relativeCreated is in milliseconds
        total_seconds = record.relativeCreated / 1000
        minutes = int(total_seconds // 60)
        seconds = total_seconds % 60
        return f"{minutes}m {seconds:.3f}s"


class CustomLogger(logging.Logger):
    """
    Custom logger class that uses the CustomRelativeFormatter.
    
    Attributes:
        level (int): The logging level for the logger.

    format:
        '[%(asctime)s]: %(message)s'
    datefmt:
        '%H:%M:%S'
    """
    
    def __init__(self, level=logging.INFO):
        super().__init__(level)
        self.setLevel(level)
        handler = logging.StreamHandler()
        formatter = CustomRelativeFormatter('[%(asctime)s]: %(message)s')
        handler.setFormatter(formatter)
        self.addHandler(handler)