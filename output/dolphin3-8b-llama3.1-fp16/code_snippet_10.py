from typing import Union

@app.post('/')
def main(user: Union[str, int]):
    return user