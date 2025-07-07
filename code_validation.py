from pathlib import Path
import os
import subprocess


models = os.listdir('output')
#print(models)

def checkSQL_Validation(modelFolder: str) -> bool:
    """
    Checks wether SQL files are valid SQl.

    Args:
        modelFolder (str): The intended models output to check.
    Output:
        Boolean (bool): Returns true if any sql files contains errors, false if all files are valid. 
    """
    path = 'output/' + modelFolder
    files = os.listdir(path)
    sqlFiles = set()
    file_with_error = set()

    # -- Retrieve SQL files for validation --
    for file in files:
        if file.endswith('.sql'):
            sqlFiles.add(file)

    # -- Check SQL validation --
    for file in sqlFiles:
        try:
            subprocess.run(
                ["py","-m","sqlfluff","lint",f"output/{modelFolder}/{file}","--dialect","ansi"],
                check=True
                )
        except:
            file_with_error.add(file)
            continue
    
    return True if len(file_with_error)>0 else False

def checkPython_Validation(modelFolder: str) -> bool:
    path = 'output/' + modelFolder
    files = os.listdir(path)
    pythonFiles = set()
    files_with_error = set()

    # -- Retrieve Python files for validation
    for file in files:
        if file.endswith('.py'):
            pythonFiles.add(file)

    for file in pythonFiles:
        with open(Path(path)/file, 'r', encoding='utf-8') as f:
            sourceFile = f.read()
        try:
            compile(source=sourceFile, filename=file, mode='exec')
        except SyntaxError as e:
            files_with_error.add(file)
            continue
    print(files_with_error)
    return True if len(files_with_error)>0 else False

def checkJava_Validation(modelFolder: str) -> bool:
    path = "output/" + modelFolder
    files = os.listdir(path=path)
    javaFiles = set()
    files_with_error = set()

    # -- Retrieve Java files for validation
    for file in files:
        if file.endswith('.java'):
            javaFiles.add(file)
    
    for file in javaFiles:
        try:
            subprocess.run(
                ['javac', f'output/{modelFolder}/{file}'], 
                capture_output=True, 
                text=True
                )
        except:
            files_with_error.add(file)
            continue
    
    return True if len(files_with_error)>0 else False

def checkJS_Validation(modelFolder: str) -> bool:
    path = "output/" + modelFolder
    files = os.listdir(path=path)
    jsFiles = set()
    files_with_error = set()

    for file in files:
        if file.endswith(".js"):
            jsFiles.add(file)
    
    for file in jsFiles:
        try:
            subprocess.run(
                ['node', f'output/{modelFolder}/{file}'],
                capture_output=True,
                text=True
                )
        except:
            files_with_error.add(file)
            continue
    
    return True if len(files_with_error)>0 else False

if __name__ =='__main__':
    for model in models:
        print(model)
        #print(f'The model: {model} has invalid sql?: {checkSQL_Validation(modelFolder=model)}')
        #print(checkPython_Validation(modelFolder=model))
        #print(checkJava_Validation(modelFolder=model))
        print(checkJS_Validation(modelFolder=model))