from fastapi import FastAPI

app = FastAPI()

@app.get("/check")
async def check():
    return {"msg": "Healthy!"}