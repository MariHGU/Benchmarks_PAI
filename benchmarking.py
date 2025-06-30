import time
import random
import os
import pandas as pd
import asyncio
from ollama import AsyncClient
from ollama import ChatResponse
from openpyxl import load_workbook

# Initialize the client with appropriate host and authorization token
def get_api_key(file_path='.api_key'):
    try:
        with open(file_path, 'r') as f:
            api_key = f.read().strip()
        return api_key
    except FileNotFoundError:
        print(f"API key file not found: {file_path}")
        raise

# Get the API key from a file outside the git repo
api_key_file = r'C:\Users\mgusdal\OneDrive - Norsk helsenett SF\Skrivebord\Benchmarkin_PAI\.api_key'
api_key = get_api_key(api_key_file)

client = AsyncClient(
    host="https://chat.nhn.no/ollama",
    headers={
        'Authorization': f'{api_key}'
    }
)

# Function to call LLM-api
async def call_llm_api(prompt):
    try:
        response: ChatResponse = await client.chat(
            model='nhn-small:latest', 
            messages=[{
                'role': 'user',
                'content': prompt,
            }],
            options= {
                "num_ctx": 40960 # Context window or add other parameters to test (i.e. thinking etc.)
            },
            stream=False
        )

        # Extract and return the message content from the response
        if hasattr(response, 'message') and hasattr(response.message, 'content'):
            response_ps = response.eval_count / (response.eval_duration / 1e9)
            prompt_ps = response.prompt_eval_count / (response.prompt_eval_duration / 1e9)
            return response.message.content, response.model, response.total_duration, response.load_duration, response.prompt_eval_count, response.prompt_eval_duration, prompt_ps, response.eval_count, response.eval_duration, response_ps
        else:
            print("Failed to parse message content")
            return None

    except ValueError as e:
        print(f"An error occurred while parsing JSON: {e}")
        return None
    except Exception as e:
        print(f"An error occurred while calling the API: {e}")
        return None

def read_prompts(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file.readlines()]

# List of prompts to test the model
prompts = read_prompts('Benchmarks_PAI/prompts/text_prompts.txt')

# Test LLM performance
async def test_llm_performance(prompts, num_tests=6):
    total_time = 0
    total_response_tokens_ps = 0
    total_api_time = 0
    for i in range(num_tests):
        prompt = prompts[i]
        start_time = time.time()
        # Call LLM-api
        response, model, totalt_duration, load_duration, prompt_token, prompt_eval_duration, prompt_ps, response_token, response_eval_duration, response_ps,  = await call_llm_api(prompt)
        end_time = time.time()
        elapsed_time = end_time - start_time
        total_time += elapsed_time
        total_api_time += totalt_duration/1e6
        total_response_tokens_ps += response_ps

        if response:
            print(f"Test #{i+1}: Prompt='{prompt[:50]}', Response='{response}...', Time={elapsed_time:.4f}s")
            print(f"Prompt_tokens={prompt_token}, Prompt_token/s={prompt_ps:.4f}, Response_tokens={response_token}, Response_token/s={response_ps:.4f} \n")

            # Write individual params to file here
            # ...
            ny_data = pd.DataFrame({
                'Model': [model],
                'Prompt nr':[i] , 
                'Total Duration': [totalt_duration/1e6], 
                'Load Duration':[load_duration/1e6], 
                'Promt Eval Count':[prompt_token], 
                'Prompt eval duration':[prompt_eval_duration/1e6], 
                'Prompt eval rate':[prompt_ps],  
                'Eval Count':[response_token], 
                'Eval duration':[response_eval_duration/1e6], 
                'Eval rate':[response_ps]
                })
            write_to_xcl(ny_data=ny_data, file_name='Benchmarks.xlsx', sheet='Sheet1')

        else:
            print(f"Test #{i+1}: Prompt='{prompt}' No response received. Time={elapsed_time:.4f}s")

    average_time = total_time / num_tests
    average_token_ps = total_response_tokens_ps / num_tests
    average_api_time = total_api_time / num_tests
    print(f"\nAverage response time over {num_tests} tests: {average_time:.4f} seconds")
    print(f"Average response tokens/s: {average_token_ps:.4f}")
    return average_time, average_token_ps, average_api_time


# Ny data du vil legge til

def write_to_xcl(ny_data, file_name, sheet):
    # Last eksisterende arbeidsbok
    filnavn = file_name
    arknavn = sheet
    workbook = load_workbook(filnavn)

    if arknavn in workbook.sheetnames:
        sheet = workbook[arknavn]
        startrow = sheet.max_row
    else:
        sheet = workbook.create_sheet(arknavn)
        startrow = 0

    # Bruk ExcelWriter i append-modus uten å sette writer.book
    with pd.ExcelWriter(filnavn, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
        ny_data.to_excel(writer, sheet_name=arknavn, index=False, header=False, startrow=startrow)


# Run the test
if __name__ == "__main__":
    # Uncomment to initiate new excel:
    df = pd.DataFrame({
        'Model': [],
        'Prompt nr':[],
        'Total Duration[ms]': [],
        'Load Duration[ms]':[],
        'Promt Eval Count':[],
        'Prompt eval duration':[],
        'Prompt eval rate':[],
        'Eval Count':[],
        'Eval duration':[],
        'Eval rate':[]
    })

    avg_df = pd.DataFrame({
        'Average time (experienced)': [],
        'Average tokens/s':[],
        'Average Time (API)': []
    })

    with pd.ExcelWriter('Benchmarks.xlsx') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
        avg_df.to_excel(writer, index=False, sheet_name='Sheet2')

    # Test and write to file
    avg_time, avg_token_ps, avg_api_time = asyncio.run(test_llm_performance(prompts))
    ny_data = pd.DataFrame({
        'Average time': [round(avg_time,4)], 
        'Average tokens/s': [round(avg_token_ps,4)], 
        'Average Time (API)': [round(avg_api_time, 4)]
        })

    write_to_xcl(ny_data=ny_data, file_name='Benchmarks.xlsx', sheet='Sheet2')