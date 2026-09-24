from sqlmodel import Field, Relationship, SQLModel
from typing import TYPE_CHECKING
from .recipeingredientlink import RecipeIngredientLink
from .stepingredientlink import StepIngredientLink

if TYPE_CHECKING:
    from .recipes import Recipe
    from .steps import Step


class Ingredient(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True, nullable=False)
    category_id: int = Field(default=None, foreign_key="category.id", nullable=True)

    recipes: list["Recipe"] = Relationship(back_populates="ingredients", link_model=RecipeIngredientLink)
    steps: list["Step"] = Relationship(back_populates="ingredients", link_model=StepIngredientLink)