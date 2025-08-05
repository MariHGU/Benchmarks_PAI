@app.post('/')
def main(data: UserData):
    return data