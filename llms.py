import os
from typing import Optional, Tuple, Union, Dict 
from deepeval.models import DeepEvalBaseLLM, OllamaModel
from ollama import Client, AsyncClient
from ollama import ChatResponse
from groq import Groq, AsyncGroq
from pydantic import BaseModel

BASE_URL = "https://beta.chat.nhn.no/ollama"
MODEL = "devstral:24b-small-2505-q8_0"
JUDGE_SEED = 42
JUDGE_TEMPERATURE = 0.7
JUDGE_MODEL = "deepseek-r1:32b-qwen-distill-fp16" # OLLAMA MODEL
# JUDGE_MODEL = "llama-3.3-70b-versatile" # GROQ MODEL

def load_api_key(path: str = ".api_key.txt") -> str:
    """
    Load the API key from a specified file.
    
    Args:
        path (str): The file path to the API key. Defaults to ".api_key.txt".
    Returns:
        str: The API key read from the file.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"API key file not found: {path}")

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
            model: str = MODEL, 
            base_url: str = BASE_URL,
            seed: int = None,
            temperature: float = None,
            ):
        self.model_name_ = model
        super().__init__(model=model, base_url=base_url)
        self.seed = seed
        self.temperature = temperature

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
    
    def generate(
        self, prompt: str, schema: Optional[BaseModel] = None
    ) -> Tuple[Union[str, Dict], float]:
        chat_model = self.load_model()
        response: ChatResponse = chat_model.chat(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            format=schema.model_json_schema() if schema else None,
            options={
                "temperature": self.temperature,
                "seed": self.seed
                     },
        )
        return (
            (
                schema.model_validate_json(response.message.content)
                if schema
                else response.message.content
            ),
            0,
        )

    async def a_generate(
        self, prompt: str, schema: Optional[BaseModel] = None
    ) -> Tuple[str, float]:
        chat_model = self.load_model(async_mode=True)
        response: ChatResponse = await chat_model.chat(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            format=schema.model_json_schema() if schema else None,
            options={
                "temperature": self.temperature,
                "seed": self.seed
                     },
        )
        return (
            (
                schema.model_validate_json(response.message.content)
                if schema
                else response.message.content
            ),
            0,
        )

    def get_model_name(self) -> str:
        return self.model_name_

    def get_seed(self) -> int:
        return self.seed
    
    def get_temperature(self) -> float:
        return self.temperature

class GroqModel(DeepEvalBaseLLM):
    """A class to interact with Groq's LLMs.
    This class extends DeepEvalBaseLLM to provide methods for generating text
    using Groq's API.
    
    Attributes:
        model_name (str): The name of the Groq model to use.
    
    """
    def __init__(self, 
                 model_name: str = JUDGE_MODEL, 
                 async_mode: bool = False, 
                 seed: int = JUDGE_SEED,
                 temperature: float = JUDGE_TEMPERATURE,
                 ):
        super().__init__(model_name=model_name)
        self.seed = seed
        self.temperature = temperature

    def load_model(self, async_mode: bool = False) -> Groq:
        api_key = load_api_key(path=".groq_api_key.txt")
        if not async_mode:
            return Groq(api_key = api_key)
        else:
            return AsyncGroq(api_key = api_key)
        
    def generate(self, prompt: str) -> str:
        groq_client = self.load_model(async_mode=False)
        response = groq_client.chat.completions.create(
            messages= [{
                "role": "user", 
                "content": prompt,
            }],
            seed= self.seed,
            temperature= self.temperature,
            model=self.model_name,
        )
        return response.choices[0].message.content
    
    async def a_generate(self, prompt: str) -> str:
        groq_client = self.load_model(async_mode=True)
        response = await groq_client.chat.completions.create(
            messages= [{
                "role": "user", 
                "content": prompt,
            }],
            seed= self.seed,
            temperature= self.temperature,
            model=self.model_name,
        )
        return response.choices[0].message.content
    
    def get_model_name(self) -> str:
        return self.model_name
    
    def get_seed(self) -> int:
        return self.seed
    
    def get_temperature(self) -> float:
        return self.temperature