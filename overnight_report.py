r"""
I've put as much as possible in a single script, too many files creates a mess ¯\_(ツ)_/¯

Use the VS code folding regions (#region <name> <code> #endregion) to hide/view sections of code.

Edit global variables (max number of runs, end time tomorrow) in the #region global variables.

run with `$ python3 overnight_report.py`

results in ./results_<date>
"""

#TODO automatisk teste de modellene som hentes (de som støtter chat i hvert fall), importere use_case_metrics, samle til pdf?




#region global variables

max_n = 2 #maximum number of test runs before generating a report. Greater than 5
date_str = ""  #Set on format DD_MM_YYYY. Leave empty for today
end_at = (7, 30) #(hour, minute) to stop testing and generate report
gather_data = False # If false: skips testing. Useful if you already have a dataset. If True: run all tests
visualize = False #If false: skips visualization




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
from contextlib import closing
import matplotlib.pyplot as plt

if not date_str:
    date_str = str(date.today().strftime('%d_%m_%Y'))



#endregion

#region initializing

def init_directory():
    """
    Initializes a name for todays directory "/results_<date>"

    Returns
    ---
    dir_str: str
        Directory name
    """
    dir_str = 'results_' + date_str

    try:
        os.mkdir(dir_str)
    except FileExistsError:
        pass

    plot_dir_str = dir_str + '/plots'        

    try:
        os.mkdir(plot_dir_str)
    except FileExistsError:
        pass

    return dir_str


def init_db(dir_str):
    """
    Initializes a SQLite database to save results from tests

    Parameters
    ---
    dir_str: str
        Directory name


    Returns
    ---
    conn: SQLite connection
        connection to the database

    """


    db_path_str = dir_str + '/data.db'

    conn = sqlite3.connect(db_path_str)
    return conn

async def get_available_models(client):
    """
    Async call API through client and fetch available models

    Parameters
    ---
    client: ollama.Client
        authenticated call to ollama server
    
    Returns
    ---
    list[str]
        list of current model names
    
    
    """

    try:
        response: ChatResponse = await client.list()
        # Extract and return the message content from the response
        if hasattr(response, 'models'):
            return [model.model for model in response.models]
        else:
            print("Failed to parse message content")
            return None

    except ValueError as e:
        print(f"An error occurred while parsing JSON: {e}")
        return None
    except Exception as e:
        print(f"An error occurred while calling the API: {e}")
        return None



async def get_chat_models(client):
    """
    Gathers all available models and checks whether they support chat

    As it turns out this takes a very long time since ollama has to load each model in and out of memory.
    Using this during working hours might be slow and disruptive


    Parameters
    ---
    client: ollama.Client
        authenticated call to ollama server
    
    Returns
    ---
    list[str]
        list of model names, which supports chat
    
    """

    all_models = await get_available_models(client)

    chat_models = []

    for model in all_models:
        res = await call_llm_api("hello", model)
        if res:
            chat_models.append(model)
            print("Model " + model + " answers chat")


#endregion

#region benchmarking

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
            print(f"Prompt_tokens={prompt_token}, Prompt_token/s={prompt_ps:.4f}, Response_tokens={response_token}, Response_token/s={response_ps:.4f} \n")
        else:
            print(f"Test #{i+1}: Prompt='{prompt}' No response received. Time={experienced_time:.4f}s")

    new_data = pd.DataFrame({
        'model': [model],
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

#region use_case_metrics

#endregion

#region plots

def get_tests_categories(conn):
    """
    Returns a list of the names of the performed tests in the database

    Parameters
    ---
    conn: sqlite3.Connection
        connection to database
    
    Returns
    ---
    test_categories: list[str]
        list of names of performed tests (= table names)
    
    """
    with closing(conn.cursor()) as cur:
        test_categories = cur.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        return [category_tuple[0] for category_tuple in test_categories]




def get_measures(conn, category_name):
    """
    Fetches the numeric measures from a single test. As some test measures multiple metrics we might want to plot

    Parameters
    ---
    conn: sqlite3.Connection
        connection to database

    category_name: str
        name of test (table in the database)


    Returns
    ---
    measures: list[str]
        the columns of the table    
    
    """
    numerics = {'INTEGER', 'REAL', 'NUMERIC'}
    measures = []

    with closing(conn.cursor()) as cur:

        cur.execute(f"PRAGMA table_info({category_name});")
        columns_info = cur.fetchall()

        for col in columns_info:
            col_name = col[1]
            col_type = col[2].upper()
            if any(ntype in col_type for ntype in numerics):
                measures.append(col_name)
    return measures

def boxplot(conn, category_name, measure, ax):
    """
    collects appropriate data and adds a boxplot to the specified plt-axis

    Parameters
    ---
    conn: sqlite3.Connection
        connection to database
    category_name: str
        name of test (table in the database)
    measure: str
        a measure during the test, i.e. a db attribte
    ax: plt axis
        where to create the boxplot
    """
    with closing(conn.cursor()) as cur:

        models = get_tested_models(conn, category_name)

        boxplot_data = []
        labels = []

        for m in models:

            cur.execute(f"SELECT {measure} FROM {category_name} WHERE model = '{m}';")
            results = [row[0] for row in cur.fetchall()]
            if results:
                boxplot_data.append(results)
                labels.append(m)

    ax.boxplot(boxplot_data, showcaps = False, showmeans = True)
    ax.set_xticklabels(labels, rotation = 45, ha = 'right')


def get_tested_models(conn, category_name):
    """
    Returns the model names in this test

    Parameters
    ---
    conn: sqlite3.Connection
        connection to database
    category_name: str
        name of test (table in the database)

    Returns
    ---
    models: list[str]
        list of model names

    """
    with closing(conn.cursor()) as cur:
        cur.execute(f"SELECT DISTINCT model FROM {category_name};")  
        models = [row[0] for row in cur.fetchall()]
    return models






def plot_test_category(conn, category_name):
    """
    creates boxplots for a test category automatically

    Parameters
    ---
    conn: sqlite3.Connection
        connection to database
    category_name: str
        name of test (table in the database)
    
    """

    measures = get_measures(conn, category_name)
    n_measures = len(measures)
    n_models = len(get_tested_models(conn, category_name))
    axs = []

    fig = plt.figure(layout = "constrained")
    fig.set_figheight(3 * n_measures)
    fig.set_figwidth(1 * n_models)

    for i, measure in enumerate(measures):
        ax = plt.subplot2grid((n_measures, 1), (i, 0))
        boxplot(conn, category_name, measure, ax)
    
    plt.savefig(dir_str + '/plots/' + category_name + '.png')
    

#endregion

#region generate report

#endregion

#region SQLite to csv (in case anyone wants to use excel)

#endregion

#region main

if __name__ == "__main__":

    #initialize
    api_key = load_api_key('.api_key.txt')

    client = AsyncClient(
        host="https://beta.chat.nhn.no/ollama",
        headers={
            'Authorization': f'Bearer {api_key}'
        }
    )   
    dir_str = init_directory()
    conn = init_db(dir_str)


    if gather_data:
        #Run until at latest specified time tomorrow
        now = datetime.now()
        tomorrow = now + timedelta(days=1)
        end_time = datetime(year=tomorrow.year, month=tomorrow.month, day=tomorrow.day, hour= end_at[0], minute=end_at[1])
        n = 0

        #collect models
        model_names = asyncio.run(get_chat_models(client))
        
        while n < max(max_n, 5) and datetime.now() < end_time:


            print("The time is " + str(datetime.now()) + ", Running experiment replication " + str(n))
            purpose, prompts = initPurpose(purp='coding')
            results = asyncio.run(multiple_test_llm_performance(prompts, purpose, model_names))
            for df in results:
                df.to_sql('coding_time', conn, if_exists = 'append', index = False)

            n += 1
        
        
    if visualize:
        plt.style.use('ggplot')

        test_categories = get_tests_categories(conn)

        for category in test_categories:
            plot_test_category(conn, category)
    

        



#endregion