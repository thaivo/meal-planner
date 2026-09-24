
from sqlmodel import Field, SQLModel


class Category(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True, nullable=False)
    description: str = Field(default=None, nullable=True)