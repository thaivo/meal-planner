from typing import Annotated

from fastapi import FastAPI, Query
from routers import meals 

app = FastAPI()
app.include_router(meals.router)


@app.get("/")
async def root():
    return {"message": "Welcome to the Meal Planner!"}