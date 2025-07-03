import re
from pathlib import Path

LANG_EXTENSION_MAP = {
    "python": "py",
    "javascript": "js",
    "typescript": "ts",
    "bash": "sh",
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


def save_code_blocks(code_blocks: list, base_filename:str="snippet", folder:str="output"):
    """
    Saves every block of code as a seperate .{lang}-file to specified folder.
    """
    Path(folder).mkdir(parents=True, exist_ok=True)

    for i, (lang, code) in enumerate(code_blocks, start=1):
        ext = LANG_EXTENSION_MAP.get(lang.lower(), "txt")
        if not lang or lang.lower() not in LANG_EXTENSION_MAP:
            unknown_lang.add(lang)
        filename = Path(folder) / f"{base_filename}_{i}.{ext}"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(code.strip())
        print(f"Lagret: {filename}")



if __name__ == "__main__":
    with open("llm_response.txt", "r", encoding="utf-8") as f:
        llm_output = f.read()

    blocks = extract_all_code_blocks(llm_output)
    
    if blocks:
        save_code_blocks(blocks, base_filename="code_snippet")
    else:
        print("Ingen kodeblokker funnet.")

    print(unknown_lang)

