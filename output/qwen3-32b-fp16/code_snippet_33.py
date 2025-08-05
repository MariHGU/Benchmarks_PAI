@app.post('/')
def main(user: dict = None):  # Accept raw dict
    return user