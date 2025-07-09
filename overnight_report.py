r"""
I've put as much as possible in a single script, too many files creates a mess ¯\_(ツ)_/¯

Use the VS code folding regions (#region <name> <code> #endregion) to hide/view sections of code.

Edit global variables (max number of runs, end time tomorrow) in the #region global variables.

run with `$ python3 overnight_report.py`

results in ./results_<date>
"""

#region global variables

max_n = 2 #maximum number of test runs before generating a report
end_at = (7, 30) #(hour, minute) to stop testing and generate report

#endregion

#region imports
import sqlite3
from datetime import datetime, timedelta, date
import os
import time
import asyncio
import pandas as pd
from pathlib import Path
from typing import List, Tuple
from ollama import AsyncClient, ChatResponse

#endregion

#region Database initializing
def init_db():
    """
    Initializes a SQLite database to save results from tests

    file:
    ./results_<date>/db_<date>.db

    """
    date_str = str(date.today().strftime('%d_%m_%Y'))
    results_date = 'results_' + date_str
    try:
        os.mkdir(results_date)
    except:
        print("Directory exists")

    db_path_str = 'results_' + date_str + '/data_' + date_str + '.db'

    conn = sqlite3.connect(db_path_str)
    cur = conn.cursor()

    cur.execute("PRAGMA foreign_keys = ON;")

    return conn


#endregion

#region time tests

"""
Based on benchmarking.py by Mari
"""

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
            response_ps = response.eval_count / (response.eval_duration / 1e9)              # Converting to seconds
            prompt_ps = response.prompt_eval_count / (response.prompt_eval_duration / 1e9)  # Converting to seconds

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
    

async def test_llm_performance(prompts: list, purpose: str, model: str) -> str:
    """
    Performs the actual testing of the model, and returns a data frame

    Input: The prompts you wish to perform the test on
    Output: The model used, the average experienced time, average api time(time retrieved from api-call) aswell as average number of generated tokens per second.
    """
    total_experienced_time = 0
    total_api_time = 0
    total_load_duration = 0
    total_prompt_tokens = 0
    total_prompt_eval_duration = 0
    total_response_tokens = 0
    total_response_eval_duration = 0

    num_tests = len(prompts)

    for i in range(num_tests):
        prompt = prompts[i]
        start_time = time.time()

        # Call LLM-api
        response, totalt_duration, load_duration, prompt_token, prompt_eval_duration, prompt_ps, response_token, response_eval_duration, response_ps,  = await call_llm_api(prompt, model=model)

        end_time = time.time()
        experienced_time = end_time - start_time
        total_experienced_time += experienced_time


        total_api_time += totalt_duration/1e9
        total_load_duration += load_duration/1e9
        total_prompt_tokens += prompt_token
        total_prompt_eval_duration += prompt_eval_duration/1e9
        total_response_tokens += response_token
        total_response_eval_duration += prompt_eval_duration/1e9


        if response:
            print(f"Test #{i+1}: Prompt='{prompt[:50]}', Response='{response[:150]}...', Time={experienced_time:.4f}s")
            print(f"Prompt_tokens={prompt_token}, Prompt_token/s={prompt_ps:.4f}, Response_tokens={response_token}, Response_token/s={response_ps:.4f} \n")
        else:
            print(f"Test #{i+1}: Prompt='{prompt}' No response received. Time={experienced_time:.4f}s")

    new_data = pd.DataFrame({
        'Model': [model],
        'total_api_time': [total_api_time],
        'total_load_duration': [total_load_duration],
        'total_prompt_tokens': [total_prompt_tokens],
        'total_prompt_eval_duration': [total_prompt_eval_duration],
        'total_response_tokens': [total_response_tokens],
        'total_response_eval_duration': [total_prompt_eval_duration]
        })
    
    return new_data

async def multiple_test_llm_performance(prompts: list, purpose: str, model: list):



    tests_to_run =[test_llm_performance(prompts=prompts, purpose=purpose, model=coding_model) for coding_model in code_model_names]
    test_results = await asyncio.gather(*tests_to_run)
    return test_results

#endregion

#region quality tests

#endregion

#region plots

#endregion

#region generate report

#endregion

#region SQLite to csv (in case anyone wants to use excel)

#endregion

#region main

if __name__ == "__main__":
    api_key = load_api_key('.api_key.txt')

    client = AsyncClient(
        host="https://beta.chat.nhn.no/ollama",
        headers={
            'Authorization': f'Bearer {api_key}'
        }
    )   

    #Where to put data while running
    conn = init_db()

    #Set correct end time
    now = datetime.now()
    tomorrow = now + timedelta(days=1)
    end_time = datetime(year=tomorrow.year, month=tomorrow.month, day=tomorrow.day, hour=7, minute=30)
    n = 0

    #collect models
    models_df = pd.read_csv('models.csv')
    code_model_names = models_df[models_df['purpose'] != 'text']['model_name']
    text_model_names = models_df[models_df['purpose'] != 'coding']['model_name']



    while n < max_n and datetime.now() < end_time:


        print("The time is " + str(datetime.now()) + ", Running experiment replication " + str(n))

        purpose, prompts = initPurpose(purp='coding')
        results = asyncio.run(multiple_test_llm_performance(prompts, purpose, code_model_names))
        for df in results:
            df.to_sql('coding_time', conn, if_exists = 'append', index = False)

        n += 1
    
    #generate_plots()
    #generate_report()


#endregion