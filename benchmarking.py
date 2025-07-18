import os
import time
import asyncio
import pandas as pd
from pathlib import Path
from typing import List, Tuple
from ollama import AsyncClient, ChatResponse
from openpyxl import load_workbook
from code_retrieval import retrieveCode
from code_validation import runCodeValidation
from utils import write_to_xlsx, initNewExcel, TestType

filename = "test.xlsx"

# -- Initialize the client with appropriate host and authorization token --
def get_api_key(file_path='.api_key') -> str:
    try:
        with open(file_path, 'r') as f:
            api_key = f.read().strip()
        return api_key
    except FileNotFoundError:
        print(f"API key file not found: {file_path}")
        raise

# -- Get the API key from a file outside the git repo --
api_key_file = Path.cwd().parent / ".api_key"
api_key = get_api_key(api_key_file)

client = AsyncClient(
    host="https://beta.chat.nhn.no/ollama",
    headers={
        'Authorization': f'{api_key}'
    }
)

# -- Function to call LLM-api --
async def call_llm_api(prompt: str, model: str) -> str:
    try:
        response: ChatResponse = await client.chat(
            model=model, 
            messages=[{
                'role': 'user',
                'content': prompt,
            }],
            options= {
                "num_ctx": 42760 # Context window or add other parameters to test (i.e. thinking etc.)

            },
            stream=False
        )

        # Extract and return the message content from the response
        if hasattr(response, 'message') and hasattr(response.message, 'content'):
            response_ps = response.eval_count / (response.eval_duration / 1e9)              # Converting to tokens/seconds
            prompt_ps = response.prompt_eval_count / (response.prompt_eval_duration / 1e9)  # Converting to tokens/seconds

            return response.message.content, response.total_duration, response.load_duration, response.prompt_eval_count, response.prompt_eval_duration, prompt_ps, response.eval_count, response.eval_duration, response_ps
        else:
            print("Failed to parse message content")
            return None

    except ValueError as e:
        print(f"An error occurred while parsing JSON: {e}")
        return None
    except Exception as e:
        print(f"An error occurred while calling the API: {e}")
        return None

def read_prompts(file_path: str) -> str:
    """ 
        Read prompts from seperate files
    """

    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file.readlines()]
    

# -- List of prompts to test the model --
def initPurpose(purp: str) -> Tuple[str, List[str]]:
    """
    Sets purpose for LLM test
    Either 'text' or 'code'
    """
    if not (purp == 'text' or purp == 'coding'):
        raise ValueError('Invalid purpose. \n Purpose has to be either "coding" or "text".')
    else:
        purpose = purp
        prompts = read_prompts('prompts/'+ purp + '_prompts.txt')
        return purpose, prompts

def write_to_txt(purpose: str, response: str):
    """
    Writes coding related response to llm_response.txt
    """
    if purpose == 'coding':
        with open("llm_response.txt", "a", encoding="utf-8") as f:
            f.write(response)


# -- Test LLM performance --
async def test_llm_performance(prompts: list, purpose: str, model: str, TestType: TestType) -> pd.DataFrame:
    """
    Performs the actual testing of the model, and writes individual prompt-performance to excel file.

    Input: The prompts you wish to perform the test on.
    Output: The model used, the average experienced time, average api time(time retrieved from api-call) aswell as average number of generated tokens per second.
    """
    if purpose == 'coding':
        with open("llm_response.txt", "w", encoding="utf-8") as f:
            f.write(f'{model}\n')

    total_time = 0
    total_response_tokens_ps = 0
    total_api_time = 0

    num_tests = len(prompts)

    digest, kv_cache = retrieveModel(model)


    for i in range(num_tests):
        prompt = prompts[i]
        start_time = time.time()

        # Call LLM-api
        response, totalt_duration, load_duration, prompt_token, prompt_eval_duration, prompt_ps, response_token, response_eval_duration, response_ps  = await call_llm_api(prompt, model=model)

        end_time = time.time()
        elapsed_time = end_time - start_time
        total_time += elapsed_time
        total_api_time += totalt_duration/1e9
        total_response_tokens_ps += response_ps

        if response:
            print(f"Test #{i+1}: Prompt='{prompt[:50]}', Response='{response[:150]}...', Time={elapsed_time:.4f}s")
            print(f"Prompt_tokens={prompt_token}, Prompt_token/s={prompt_ps:.4f}, Response_tokens={response_token}, Response_token/s={response_ps:.4f} \n")

            # Write individual params to file here
            ny_data = pd.DataFrame({
                'Model': [model],
                'Digest': [digest],
                'KV Cache Type': [kv_cache],
                'Prompt nr':[i], 
                'Total Duration': [round(totalt_duration/1e6)], 
                'Load Duration':[round(load_duration/1e6)], 
                'Promt Eval Count':[prompt_token], 
                'Prompt eval duration':[round(prompt_eval_duration/1e6)], 
                'Prompt eval rate':[round(prompt_ps)],  
                'Eval Count':[response_token], 
                'Eval duration':[round(response_eval_duration/1e6)], 
                'Eval rate':[round(response_ps)],
                'Intended Purpose': [purpose]
                })
            
            write_to_xlsx(df=ny_data, file_name=filename, sheet_name='Benchmarks', test_type=TestType)

            write_to_txt(purpose=purpose, response=response)

        else:
            print(f"Test #{i+1}: Prompt='{prompt}' No response received. Time={elapsed_time:.4f}s")

    average_time = round(total_time / num_tests)
    average_token_ps = round(total_response_tokens_ps / num_tests)
    average_api_time = round(total_api_time / num_tests)

    print(f"\nAverage response time over {num_tests} tests: {average_time:.4f} seconds")
    print(f"Average response tokens/s: {average_token_ps:.4f}")

    ny_data = pd.DataFrame({
        'Model': [model],
        'Digest': [digest],
        'KV Cache Type': [kv_cache],
        'Average time': [average_time], 
        'Average tokens/s': [average_token_ps], 
        'Average Time (API)': [average_api_time],
        'Inteded purpose': [purpose],
        'Language errors': [1]      # Default value for non-coding prompts
        })

    print('Test completed')
    return ny_data

# -- Retrieve model-info --
def retrieveModel(modelName: str) -> Tuple[str, str]:
    """
    Retrieves saved KV_Cache and digest from csv file
    """
    df = pd.read_csv(r'models.csv')
    
    match = df[df['model_name'] == modelName]

    if not match.empty:
        digest = match.iloc[0]['digest_nr']
        kv_cache = match.iloc[0]['kv_cache']
        return digest, kv_cache
    else:
        raise NameError(f"Did not find model: {modelName}")
    
async def initBenchmarking(newExcel: bool = False):
    purps = ['coding', 'text']
    models = ['cogito:32b-v1-preview-qwen-fp16','hermes3:70b-llama3.1-fp16']
    TestType = 4
    

    avg_df = pd.DataFrame({
        'Model':[],
        'Digest': [],
        'KV Cache Type': [],
        'Average time (experienced)[s]': [],
        'Average tokens/s':[],
        'Average Time (API)[s]': [],
        'Inteded purpose': [],
        'Language errors': []
    })

    filepath = Path("results")/"avg_results.csv"

    if not filepath.exists():
        avg_df.to_csv(filepath, index=False)
    

    if newExcel == True:
        initNewExcel(test_type=TestType, fileName=filename)

    # Test and write to file
    for model in models:

        for purp in purps:
            purpose, prompts = initPurpose(purp=purp)
            df = await test_llm_performance(prompts, purpose, model=model, TestType=TestType)
            if purp == 'coding':
                retrieveCode()
                
                validateCode = input('Run code validation? [y/n]: ')

                if validateCode == 'y':
                    #call code validation
                    df['Language errors'] = runCodeValidation(model=model.replace(':','-'))
                    print(df)

            df.to_csv(filepath, mode='a', index=False, header=False)
            write_to_xlsx(df=df, file_name=Path("test.xlsx"), sheet_name="Avg_Benchmarks", test_type=TestType)
            



# Run the test
if __name__ == "__main__":

    asyncio.run(initBenchmarking(newExcel=False))
        