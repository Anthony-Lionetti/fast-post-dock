from fastapi import FastAPI
from . import models
from .database import engine
from .routers import auth, user

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(user.router)

@app.get("/check")
async def check():
    return {"msg": "Healthy!"}