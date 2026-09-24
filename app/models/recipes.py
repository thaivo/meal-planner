from sqlmodel import Field, Relationship, SQLModel
from typing import TYPE_CHECKING
from .recipeingredientlink import RecipeIngredientLink

if TYPE_CHECKING:
    from .ingredients import Ingredient

class Recipe(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str = Field(index=True, nullable=False)
    description: str = Field(default=None, nullable=True)

    ingredients: list["Ingredient"] = Relationship(back_populates="recipes", link_model=RecipeIngredientLink)