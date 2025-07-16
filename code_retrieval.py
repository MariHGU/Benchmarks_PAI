import os
import re
from pathlib import Path

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


def extract_all_code_blocks(response_text: str):
    """
    Extracts all blocks of code
    Removes ``` and returns only the code itself.
    """
    # Ekstraher kodeblokker som starter med ```<språk>
    pattern = r"```(\w+)?\n(.*?)```"
    matches = re.findall(pattern, response_text, re.DOTALL | re.IGNORECASE)
    return matches


def save_code_blocks(code_blocks: list, model: str):
    """
    Saves every block of code as a seperate .{lang}-file to specified folder.
    """
    base_filename = "code_snippet"

    Path("output").mkdir(parents=True, exist_ok=True)
    model_folder = model.replace(':', '-').strip('\n')

    folder = Path("output") / model_folder
    Path(folder).mkdir(parents=True, exist_ok=True)

    for i, (lang, code) in enumerate(code_blocks, start=1):

        ext = LANG_EXTENSION_MAP.get(lang.lower(), "txt")   # Defaults to .txt file

        if (lang.lower() not in LANG_EXTENSION_MAP) and lang != '':
            unknown_lang.add(lang)                          # Store unknown languages to add to dictionary if necessary
        filename = Path(folder) / f"{base_filename}_{i}.{ext}"

        with open(filename, "w", encoding="utf-8") as f:
            f.write(code.strip())
        print(f"Lagret: {filename}")

def read_output():
    """
        Retrieves output and model from llm_output
    """
    with open("llm_response.txt", "r", encoding="utf-8") as f:
        llm_output = f.read()
        f.seek(0)
        model = f.readline()

    return llm_output, model

def retrieveCode():
    llm_output, model = read_output()

    print(f'Retrieving code from the model: {model} \n')

    blocks = extract_all_code_blocks(llm_output)
    
    if blocks:
        save_code_blocks(blocks, model=model)
    else:
        print("Ingen kodeblokker funnet.")
    
    if (len(unknown_lang) > 0):
        print(f'\nThe following unknown languages where found: {unknown_lang}')
        print("Consider adding to language dictionary, or handle manually.\n")

    remove = input("Delete textfile? [y/n]: ")
    if remove == 'y':
        os.remove('llm_response.txt')


if __name__ == "__main__":

    retrieveCode()
