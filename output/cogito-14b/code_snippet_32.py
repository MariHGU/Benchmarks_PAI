@app.post("/")
async def main(user_data: dict):
    return {"received_user": user_data.get("user")}