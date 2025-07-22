import os
import re
from pathlib import Path
from typing import Tuple

LANG_EXTENSION_MAP = {
    "python": "py",
    "javascript": "js",
    "typescript": "ts",
    "bash": "sh",
    "sh": "sh",
    "shell": "sh",
    "sql": "sql",
    "html": "html",
    "css": "css",
    "json": "json",
    "java": "java",
    "c++": "cpp",
    "cpp": "cpp",
    "c": "c",
    "csharp": "cs",
    "go": "go",
    "ruby": "rb",
    "rust": "rs",
    "php": "php",
    "yaml": "yml",
    "kotlin":"kt",
    "scss": "scss",
    "xml": "xml",
    "xsl": "xsl",
    "xslt": "xslt"
}

unknown_lang = set()

def extract_all_code_blocks(response_text: str) -> list:
    """
    Extracts all blocks of code from the text that are not within <think>...</think>.
    
    Args:
        response_text (str): String of entire llm_response to the coding prompts.
    Returns:
        matchers (list): List of all code snippets found in llm_response.
    """
    # 1. Fjerner <think>...</think>-blokker
    cleaned_text = re.sub(r"<think>.*?</think>", "", response_text, flags=re.DOTALL | re.IGNORECASE)

    # 2. Ekstraher kodeblokker (```<språk>\n<kode>```)
    pattern = r"```[ \t]*([\w+-]*)\s*\n(.*?)```"
    matches = re.findall(pattern, cleaned_text, re.DOTALL | re.IGNORECASE)

    return matches



def save_code_blocks(code_blocks: list, model: str) -> None:
    """
    Saves every block of code as a seperate .{lang}-file to specified folder.

    Args:
        code_blocks (list): List of code_snippets extracted from llm_response.
        model (str): Name of model who generated the code.
    """
    base_filename = "code_snippet"
    folderName = "output"

    Path(folderName).mkdir(parents=True, exist_ok=True)
    model_folder = model.replace(':', '-').strip('\n')

    folder = Path(folderName) / model_folder
    Path(folder).mkdir(parents=True, exist_ok=True)

    for i, (lang, code) in enumerate(code_blocks, start=1):

        ext = LANG_EXTENSION_MAP.get(lang.lower(), "txt")   # Defaults to .txt file

        if (lang.lower() not in LANG_EXTENSION_MAP) and lang != '':
            unknown_lang.add(lang)                          # Store unknown languages to add to dictionary if necessary
        filename = Path(folder) / f"{base_filename}_{i}.{ext}"

        with open(filename, "w", encoding="utf-8") as f:
            f.write(code.strip())
        print(f"Lagret: {filename}")

def read_output() -> Tuple[str, str]:
    """
        Retrieves output and model from llm_output

        Returns:
            llm_output (str): String of llm_output.
            model (str): Name of model who genereated response.
    """
    with open("llm_response.txt", "r", encoding="utf-8") as f:
        llm_output = f.read()
        f.seek(0)
        model = f.readline()

    return llm_output, model

def retrieveCode() -> None:
    """
    Initiates retrieval of code from llm_response.
    """
    llm_output, model = read_output()

    print(f'Retrieving code from the model: {model} \n')

    blocks = extract_all_code_blocks(llm_output)
    
    if blocks:
        save_code_blocks(blocks, model=model)
    else:
        print("No codeblock were found in llm_resposne.")
    
    if (len(unknown_lang) > 0):
        print(f'\nThe following unknown languages where found: {unknown_lang}')
        print("Consider adding to language dictionary, or handle manually.\n")

    remove = input("Delete textfile? [y/n]: ")

    while remove != 'y' and remove != 'n':
        print(f'Invalid input: "{remove}"')
        remove = input("Delete textfile? [y/n]: ")
    if remove == 'y':
        os.remove('llm_response.txt')


if __name__ == "__main__":

    retrieveCode()
