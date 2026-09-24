from sqlmodel import Field, Relationship, SQLModel

from app.models.recipes import Recipe
from app.models.steps import Step


class Ingredient(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True, nullable=False)
    category_id: int = Field(default=None, foreign_key="category.id", nullable=True)

    recipes: list["Recipe"] = Relationship(back_populates="ingredients", link_model="RecipeIngredientLink")
    steps: list["Step"] = Relationship(back_populates="ingredients", link_model="StepIngredientLink")