from fastapi import APIRouter
router = APIRouter(prefix="/meals", tags=["meals"])

@router.get("/")
async def get_meals():
    return {"meals": ["Pizza", "Burger", "Salad"]}

