@app.post("/")
async def main(user_data: dict):
    try:
        return {"received_user": user_data.get("user")}
    except Exception as e:
        return {"error": str(e)}, 400