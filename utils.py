import json, logging, os, requests, time
from typing import Tuple, List, Dict, Optional, Union
from deepeval.models import DeepEvalBaseLLM, OllamaModel
from ollama import Client, AsyncClient
from ollama import ChatResponse
from groq import Groq, AsyncGroq
from openpyxl import load_workbook
import pandas as pd
from pydantic import BaseModel


MODEL = "nhn-small:latest"
JUDGE_SEED = 42
JUDGE_TEMPERATURE = 0.7
JUDGE_MODEL = "nhn-small:latest" # OLLAMA MODEL
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
            model: str = "gemma3n:e4b-it-q8_0", 
            base_url: str = "https://beta.chat.nhn.no/ollama",
            api_key_file: str = ".api_key.txt",
            seed: int = None,
            temperature: float = None,
            ):
        self.model_name_ = model
        super().__init__(model=model, base_url=base_url)
        self.api_key_file = api_key_file
        # self.client = Client(host=self.base_url)
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
        print(time.strftime("[%d/%m %H:%M:%S]", time.localtime()), ": Logger initialized")



def retrieve_model_info(model_name: str = None, csv_file: str = "models.csv") -> Tuple[str, str]:
    """
    Retrieve model digest number and kv cache size from the model instance.

    Args:
        model (str): The name of the model to retrieve information from. Defaults to None.
        csv_file (str): The path to the CSV file containing model information. Defaults to "models.csv".
    Returns:
        Tuple[str, str]: A tuple containing the model digest number and kv cache size.
    """
    if not isinstance(model_name, str):
        raise TypeError("model_name must be a string")
    if not os.path.exists(csv_file):
        raise FileNotFoundError(f"CSV file not found: {csv_file}")


    models_DF = pd.read_csv("models.csv")
    
    match = models_DF[models_DF['model_name'] == model_name]

    if not match.empty:
        digest = match.iloc[0]['digest_nr']
        kv_cache = match.iloc[0]['kv_cache']
        return digest, kv_cache
    else:
        raise NameError(f"Did not find model: {model_name}")
    

def write_to_xlsx(df: pd.DataFrame, file_name: str, sheet_name: str) -> None:
    """
    Write data to an Microsoft Excel file (.xlsx), appending to a specified sheet.
    If the sheet does not exist, it will be created.
    If the file does not exist, it will be created.
    
    Args:
        new_data (pd.DataFrame): The data to write to the Excel file.
        file_name (str): The name of the Excel file.
        sheet (str): The name of the sheet to write to.
    """
    if not os.path.exists(file_name):
        with pd.ExcelWriter(file_name) as excel_writer:
            # Create a new file if it does not exist
            df_header = pd.DataFrame({
                "Model": [],
                "Digest": [],
                "KV Cache": [],
                "Prompt Number": [],
                "Judge Model": [],
                "Judge Seed": [],
                "Judge Temperature": [],
                "Score": [],
                "Reason": []
            })
            df_header.to_excel(excel_writer, sheet_name=sheet_name, index=False)
    workbook = load_workbook(file_name)

    header = False
    if sheet_name in workbook.sheetnames:
        sheet = workbook[sheet_name]
        startrow = sheet.max_row
    else:
        sheet = workbook.create_sheet(sheet_name)
        startrow = 0
        header = True

    # Use ExcelWriter in append mode without setting writer.book
    with pd.ExcelWriter(file_name, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False, header=header, startrow=startrow)

    
def log_results(
        type_of_test: str,
        model_name: str,
        results: List[tuple],
        file_name: str,
        prompt_id: int = None,
        judge_params: Tuple[str, int, float] = (JUDGE_MODEL, JUDGE_SEED, JUDGE_TEMPERATURE),
        ) -> None:
    """Log the summarization results to .xlsx file.
    Args:
        model_name (str): The name of the model used for summarization.
        results (List[tuple]): A list of tuples containing the score and reason for each prompt.
        file_name (str): The name of the file to save the results.
    Returns:
        None
    """
    if not file_name.endswith('.xlsx'):
        raise ValueError("File name is not an .xlsx file")
    if not isinstance(type_of_test, str):
        raise TypeError("type_of_test must be a string")
    
    if type_of_test.strip().lower() not in ["summarization", "prompt alignment", "alignment", "helpfulness"]:
        match type_of_test.strip().lower()[0]:
            case "s":
                sheet_name, raise_ = ("Summarization", False) if input("Are you testing summarization? [Y/n]").lower() == "y" else (type_of_test, True)
            case "p":
                sheet_name, raise_ = ("PromptAlignment", False) if input("Are you testing prompt alignment? [Y/n]").lower() == "y" else (type_of_test, True)
            case "a":
                sheet_name, raise_ = ("PromptAlignment", False) if input("Are you testing prompt alignment? [Y/n]").lower() == "y" else (type_of_test, True)
            case "h":
                sheet_name, raise_ = ("Helpfulness", False) if input("Are you testing helpfuless? [Y/n]").lower() == "y" else (type_of_test, True)
            case _:
                raise_ = True
        if raise_:
            raise ValueError("type_of_test must be one of 'summarization', 'prompt alignment', or 'helpfulness'")
    else:
        if type_of_test.strip().lower() in ["prompt alignment", "alignment"]:
            sheet_name = "PromptAlignment"
        else:
            sheet_name = type_of_test.strip().title()
    sheet_name += "Results"
    
    digest, kv_cache = retrieve_model_info(model_name=model_name)

    judge_model_name, judge_seed, judge_temp = judge_params


    for prompt_no, (score, reason) in enumerate(results):
        if prompt_id is not None:
            prompt_ref = prompt_id
        else:
            prompt_ref = prompt_no

        df_result = pd.DataFrame({
            "Model": [model_name],
            "Digest": [digest],
            "KV Cache": [kv_cache],
            "Prompt Number": [prompt_ref],
            "Judge Model": [judge_model_name],
            "Judge Seed": [judge_seed],
            "Judge Temperature": [judge_temp],
            "Score": [score],
            "Reason": [reason]
        })

        write_to_xlsx(
            df=df_result, 
            file_name=file_name, 
            sheet_name=sheet_name
        )
            
