from contextlib import asynccontextmanager
from sqlmodel import SQLModel

from typing import Annotated
from fastapi import FastAPI, Query
from .routers import meals
from .database import engine
# from .models import categories, recipes, ingredients, steps, units, recipeingredientlink, stepingredientlink
from .models import *
from sentence_transformers import SentenceTransformer

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Perform any startup tasks here
    SQLModel.metadata.create_all(engine)

    app.state.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')  # Placeholder for your embedding model, e.g., SentenceTransformer or similar
    yield
    # Perform any shutdown tasks here



app = FastAPI(lifespan=lifespan)
app.include_router(meals.router)


@app.get("/")
async def root():
    return {"message": "Welcome to the Meal Planner!"}

