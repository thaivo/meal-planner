from http.client import HTTPException

import numpy as np
from app.models.recipes import Recipe
from fastapi import APIRouter, Query, Request
from ..database  import SessionDep
from typing import Annotated
from ..models.recipes import Recipe
from ..models.steps import Step


router = APIRouter(prefix="/recipes", tags=["recipes"])

@router.get("/")
async def get_recipes(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100
) -> list[Recipe]:
    recipes = session.query(Recipe).offset(offset).limit(limit).all()
    return recipes

@router.get("/{recipe_id}")
async def get_recipe(
    session: SessionDep,
    recipe_id: int
) -> dict:
    recipe = session.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    steps = session.query(Step).filter(Step.recipe_id == recipe_id).order_by(Step.step_number).all()
    return {
        "recipe": recipe,
        "ingredients": recipe.ingredients,
        "steps": steps
    }

def cosine_similarity(vec1, vec2):
    """Compute the cosine similarity between two vectors."""
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    magnitude1 = sum(a ** 2 for a in vec1) ** 0.5
    magnitude2 = sum(b ** 2 for b in vec2) ** 0.5
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0
    return dot_product / (magnitude1 * magnitude2)

@router.get("/recommendations/")
def recommend_recipes(
    request: Request,
    session: SessionDep,
    user_craving: str
):
    """
    Recommend recipes based on the provided ingredient vector.
    The ingredient vector should be a list of floats representing the presence or quantity of ingredients.
    """
    # Convert the user craving into an ingredient vector
    user_vector = request.app.state.embedding_model.encode(user_craving).tolist()  # Assuming you have an embedding model to convert text to vector

    # Fetch all recipes and their ingredient vectors from the database
    recipes = session.query(Recipe).all()

    recommendations = []

    for recipe in recipes:
        ingredient_names = ", ".join([ingredient.name for ingredient in recipe.ingredients])
        # Assuming each recipe has an attribute `ingredient_vector` which is a list of floats

        dynamic_text_blueprint = f"Title: {recipe.title}, Description: {recipe.description}, Ingredients: {ingredient_names}"

        recipe_vector = request.app.state.embedding_model.encode(dynamic_text_blueprint).tolist()  # Assuming you have an embedding model to convert text to vector
        similarity_score = cosine_similarity(user_vector, recipe_vector)

        recommendations.append({
            "recipe_id": recipe.id,
            "title": recipe.title,
            "description": recipe.description,
            "ingredients": ingredient_names,
            "similarity_score": round(similarity_score, 4)
        })

    # Sort recommendations by similarity score in descending order
    recommendations.sort(key=lambda x: x["similarity_score"], reverse=True)

    return {"query": user_craving, "recommendations": recommendations}