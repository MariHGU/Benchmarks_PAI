r"""
I've put as much as possible in a single script, too many files creates a mess ¯\_(ツ)_/¯

Use the VS code folding regions (#region <name> <code> #endregion) to hide/view sections of code.

Edit global variables (max number of runs, end time tomorrow) in the #region global variables.

run with `$ python3 overnight_report.py`

results in ./results_<date>
"""

#region global variables

max_n = 16 #maximum number of test runs before generating a report
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
    os.mkdir(results_date)

    #db_path_str = '/results_' + date_str + '/db_' + date_str + '.db'
    db_path_str = 'results_' + date_str + '/data_' + date_str + '.db'

    print(db_path_str)


    conn = sqlite3.connect(db_path_str)
    cur = conn.cursor()

    cur.execute("PRAGMA foreign_keys = ON;")

    conn.close()


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









#endregion

#region quality tests

#endregion

#region plots

#endregion

#region generate report

#endregion

#region SQLite to csv (excel)

#endregion

#region main

if __name__ == "__main__":

    init_db()

    now = datetime.now()
    tomorrow = now + timedelta(days=1)
    end_time = datetime(year=tomorrow.year, month=tomorrow.month, day=tomorrow.day, hour=7, minute=30)
    n = 0

    while n < max_n and datetime.now() < end_time:
        print("The time is" + str(datetime.now()))

        #test_time()
        #test_helpfullness()
        #test_prompt_alignment()
        #test_summarizing()

        n += 1
    
    #generate_plots()
    #generate_report()


#endregion