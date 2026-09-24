

from sqlmodel import Field, SQLModel


class RecipeIngredientLink(SQLModel, table=True):
    recipe_id: int = Field(default=None, foreign_key="recipe.id", primary_key=True)
    ingredient_id: int = Field(default=None, foreign_key="ingredient.id", primary_key=True)
    quantity: float = Field(default=None, nullable=False)
    unit_id: int = Field(default=None, foreign_key="unit.id", nullable=True)