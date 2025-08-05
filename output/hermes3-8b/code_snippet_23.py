from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.post("/user")
def create_user(user_data):
    # Check if the user already exists in the database
    if user == "smith":
        raise HTTPException(status_code=422, detail="User already exists")

    # Save the user to the database
    # ...
    
    return {"message": "User created successfully", "user": user_data}