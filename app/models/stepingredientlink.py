
from sqlmodel import Field, SQLModel


class StepIngredientLink(SQLModel, table=True):
    step_id: int = Field(default=None, foreign_key="step.id", primary_key=True)
    ingredient_id: int = Field(default=None, foreign_key="ingredient.id", primary_key=True)
    note: str = Field(default=None, nullable=True)
    