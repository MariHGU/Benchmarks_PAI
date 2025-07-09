import os
import subprocess
import json
from pathlib import Path
from code_retrieval import LANG_EXTENSION_MAP


def createLangLists(modelFolder: str) -> dict:
    """
    Creates a dictionary containing all languages represented in the LLMs answer.

    Args: 
        modelFolder (str): the model's code you would like to retrieve.

    Output: 
        (dict): A dictionary on the format: *Language: (files: [(str)], Contains error: bool)* 
    """
    
    languageFiles = {}

    path = 'output/' + modelFolder
    files = os.listdir(path=path)

    for lang in LANG_EXTENSION_MAP.values():
        for file in files:
            if file.endswith(f'.{lang}'):
                languageFiles.setdefault(lang, {
                    'files':[], 
                    'Contains error':False
                    })
                if file not in languageFiles[lang]['files']:
                    languageFiles[lang]['files'].append(file)
    return languageFiles


models = os.listdir('output')
#print(models)

def check_sql_Validation(modelFolder: str, languageFiles: dict) -> bool:
    """
    Checks wether SQL files are valid SQl.

    Args:
        modelFolder (str): The intended models output to check.
        languageFiles (dict): The files of language for that model.
    Output:
        Boolean (bool): Returns true if any sql files contains errors, false if all files are valid. 
    """
    file_with_error = set()

    # -- Retrieve SQL files for validation --
    sqlFiles = languageFiles['sql']['files']

    # -- Check SQL validation --
    for file in sqlFiles:
        try:
            subprocess.run(
                ["py","-m","sqlfluff","lint",f"output/{modelFolder}/{file}","--dialect","mysql"],
                check=True
                )
        except:
            file_with_error.add(file)
            continue
    return True if len(file_with_error)>0 else False

def check_python_Validation(modelFolder: str, langFiles: list) -> bool:
    path = 'output/' + modelFolder
    files_with_error = set()

    # -- Retrieve Python files for validation
    pythonFiles = langFiles['py']['files']

    for file in pythonFiles:
        with open(Path(path)/file, 'r', encoding='utf-8') as f:
            sourceFile = f.read()
        try:
            compile(source=sourceFile, filename=file, mode='exec')
        except SyntaxError as e:
            files_with_error.add(file)
            continue

    return True if len(files_with_error)>0 else False

def check_java_Validation(modelFolder: str, langFiles: list) -> bool:
    files_with_error = set()

    # -- Retrieve Java files for validation --
    javaFiles = langFiles['java']['files']
    
    for file in javaFiles:
        result = subprocess.run(
                ['javac', f'output/{modelFolder}/{file}'], 
                capture_output=True, 
                text=True
                )
        if result.returncode != 0:
            files_with_error.add(file)
            
    return True if len(files_with_error)>0 else False

def check_js_Validation(modelFolder: str, langFiles: list) -> bool:
    jsFiles = langFiles['js']['files']
    files_with_error = set()
    
    for file in jsFiles:
        result = subprocess.run(
                ['node','--check', f'output/{modelFolder}/{file}'],
                capture_output=True,
                text=True
                )
        if result.returncode != 0:
            files_with_error.add(file)
            
    return True if len(files_with_error)>0 else False


def check_cpp_Validation(modelFolder: str, langFiles: list) -> bool:
    cppFiles = langFiles['cpp']['files']
    files_with_error = set()

    for file in cppFiles:
        result = subprocess.run(
                ['g++', '-fsyntax-only', f'output/{modelFolder}/{file}'],
                capture_output=True,
                text=True
            )
        if result.returncode != 0:
            files_with_error.add(file)
            
    return True if len(files_with_error)>0 else False

def check_json_validation(modelFolder: str, langFiles: list) -> bool:
    jsonFiles = langFiles['json']['files']
    files_with_error = set()

    for file in jsonFiles:
        try:
            with open(f'output/{modelFolder}/{file}') as f:
                json.load(f)
        except:
            files_with_error.add(file)

    return True if len(files_with_error)>0 else False

def check_bash_validation(modelFolder: str, LangFiles: list) -> bool:
    bashFiles = LangFiles['sh']['files']
    files_with_error = set()

    for file in bashFiles:
        result = subprocess.run(
            ['bash', '-n', f'output/{modelFolder}/{file}'],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            files_with_error.add(file)

    return True if len(files_with_error)>0 else False

def check_ts_validation(modelFolder: str, LangFiles: list) -> bool:
    tsFiles = LangFiles['ts']['files']
    files_with_error = set()

    for file in tsFiles:
        result = subprocess.run(
            [f'tsc', f'output/{modelFolder}/{file}', '--noEmit'],
            capture_output=True,
            text = True,
            shell=True
        )
        if result.returncode != 0:
            files_with_error.add(file)
    return True if len(files_with_error)>0 else False

def check_html_validation(modelFolder: str, LangFiles: list) -> bool:
    htmlFiles = LangFiles['html']['files']
    files_with_error = set()

    for file in htmlFiles:
        result = subprocess.run(
            ['htmlhint.cmd', f'output/{modelFolder}/{file}'],
            capture_output=True,
            text= True
        )
        if result.returncode != 0:
            files_with_error.add(file)
    return True if len(files_with_error)>0 else False

def check_css_validation(modelFolder: str, LangFiles: list) -> bool:
    cssFiles = LangFiles['css']['files']
    files_with_error = set()

    for file in cssFiles:
        result = subprocess.run(
            ['stylelint', f'output/{modelFolder}/{file}'],
            shell=True,
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            files_with_error.add(file)

    return True if len(files_with_error)>0 else False  

def check_c_validation(modelFolder: str, LangFiles: str) -> bool:
    cFiles = LangFiles['c']['files']
    files_with_error = set()

    for file in cFiles:
        result = subprocess.run(
            ['gcc','-fsyntax-only', f'output/{modelFolder}/{file}'],
            shell=True,
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            files_with_error.add(file)

    return True if len(files_with_error)>0 else False  

def check_cs_validation(modelFolder: str, LangFiles: str) -> bool:
    csFiles = LangFiles['cs']['files']
    files_with_error = set()

    for file in csFiles:
        result = subprocess.run(
            ['csval', f'output/{modelFolder}/{file}'],
            shell=True,
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            files_with_error.add(file)
            print(result.stderr)
            print(result.stdout)

    return True if len(files_with_error)>0 else False  

def check_go_validation(modelFolder: str, LangFiles: list) -> bool:
    goFiles = LangFiles['go']['files']
    files_with_error = set()

    for file in goFiles:
        result = subprocess.run(
            ['go', 'build','-o','NUL',f'output/{modelFolder}/{file}'],
            shell=True,
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            files_with_error.add(file)

    return True if len(files_with_error)>0 else False  

def check_ruby_validation(modelFolder: str, LangFiles: list) -> bool:
    rbFiles = LangFiles['rb']['files']
    files_with_error = set()

    for file in rbFiles:
        result = subprocess.run(
            ['ruby', '-c',f'output/{modelFolder}/{file}'],
            shell=True,
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            files_with_error.add(file)

    return True if len(files_with_error)>0 else False  



langFuncs = {
    "py": check_python_Validation,
    "js": check_js_Validation,
    "ts": check_ts_validation,
    "sh": check_bash_validation,
    "sql": check_sql_Validation,
    "html": check_html_validation,
    "css": check_css_validation,
    "json": check_json_validation,
    "java": check_java_Validation,
    "cpp": check_cpp_Validation,
    "rb": check_ruby_validation,
    "go": check_go_validation,
    "c": check_c_validation,
    "cs": check_cs_validation
}

def checkCode(modelFrame: str):
        langFiles = createLangLists(modelFolder=model)

        for lang, info in langFiles.items():
            func = langFuncs.get(lang)

            if func:
               error = func(model, langFiles)
               langFiles[lang]['Contains error'] = error
            else:
               print(f'No validation func for {lang}')

        bad_languages = set()
        for lang, info in langFiles.items():
            if langFiles[lang]['Contains error']:
                bad_languages.add(lang)

        if len(bad_languages)>0:
            print(f'The model: {model} presents code with syntax-errors from the following languages: {bad_languages}')


if __name__ =='__main__':
    for model in models:
        print(model)
        
        checkCode(modelFrame=model)
