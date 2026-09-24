
from sqlmodel import Field, Relationship, SQLModel

from .ingredients import Ingredient
from .stepingredientlink import StepIngredientLink

class Step(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    recipe_id: int = Field(default=None, foreign_key="recipe.id", nullable=False)
    step_number: int = Field(default=None, nullable=False)
    description: str = Field(default=None, nullable=False)

    ingredients: list["Ingredient"] = Relationship(back_populates="steps", link_model=StepIngredientLink)