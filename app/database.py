
from sqlmodel import Session, create_engine
from fastapi import Depends
from typing import Annotated


sqlite_url = "sqlite:///./meal_planner.db"
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})


def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]