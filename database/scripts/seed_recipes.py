import json
from pathlib import Path
from sqlmodel import Session, select, create_engine
from app.database import engine
from app.models import Recipe, Ingredient, Category, Unit, RecipeIngredientLink, StepIngredientLink, Step

def get_or_create(session: Session, model, **kwargs):
    """Helper function to fetch an existing lookup or insert it if missing."""
    instance = session.exec(select(model).filter_by(**kwargs)).first()
    if not instance:
        instance = model(**kwargs)
        session.add(instance)
        session.flush()  # Flushes to get an ID back before final commit
    return instance

def ingest_multiple_recipes_from_json(json_path: Path):
    with open(json_path, "r") as f:
        recipes_list = json.load(f)  # This is now a Python list of dictionaries

    # Loop through each individual recipe inside the array
    for recipe_data in recipes_list:
        with Session(engine) as session:
            try:
                # 1. Insert Base Recipe
                recipe = Recipe(title=recipe_data["title"], description=recipe_data["description"])
                session.add(recipe)
                session.flush()

                ingredient_id_map = {}

                # 2. Process Ingredients, Categories, and Units
                for ing in recipe_data["ingredients"]:
                    category = get_or_create(session, Category, name=ing["category"])
                    ingredient = get_or_create(session, Ingredient, name=ing["name"], category_id=category.id)
                    ingredient_id_map[ing["name"]] = ingredient.id

                    # TODO: Consider adding an abbreviation field to the Unit model if needed
                    # unit = get_or_create(session, Unit, name=ing["unit"], abbreviation=ing["unit"][:3])
                    unit = get_or_create(session, Unit, name=ing["unit"])
                    recipe_ing = RecipeIngredientLink(
                        recipe_id=recipe.id,
                        ingredient_id=ingredient.id,
                        quantity=ing["quantity"],
                        unit_id=unit.id
                    )
                    session.add(recipe_ing)

                # 3. Process Steps & Mapping Connections
                for step_data in recipe_data["steps"]:
                    instruction = Step(
                        recipe_id=recipe.id,
                        step_number=step_data["step_number"],
                        description=step_data["instruction_text"]
                    )
                    session.add(instruction)
                    session.flush()
                    
                    for ing_name in step_data["ingredients_used"]:
                        ing_id = ingredient_id_map.get(ing_name)
                        if ing_id:
                            step_ing = StepIngredientLink(
                                step_id=instruction.id,
                                ingredient_id=ing_id,
                                note=step_data["instruction_text"]
                            )
                            session.add(step_ing)

                # Commit each recipe individually so one failure doesn't ruin the entire batch
                session.commit()
                print(f"Successfully ingested: {recipe.title}")

            except Exception as e:
                session.rollback()
                print(f"Skipped '{recipe_data.get('title', 'Unknown')}'. Database rolled back. Error: {e}")


if __name__ == "__main__":
    # Example local runner execution pattern
    recipe_file = Path(__file__).parent.parent / "scripts" / "data" / "recipes.json"
    ingest_multiple_recipes_from_json(recipe_file)
