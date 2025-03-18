from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..services.user_services import find_user_by_id

class ReqUserDetails(BaseModel):
  user_id: int

class ResUserDetails(BaseModel):
  user_id: int
  full_name: str
  email: str
  difficulty_level: int
  recent_avg_res_time: float
  recent_avg_score: float

router = APIRouter()

@router.post("/user-details", response_model=ResUserDetails)
async def user_details_endpoint(request: ReqUserDetails):
  try:
    user = find_user_by_id(request.user_id)
    if user is None:
      raise ValueError("User not found")
  except Exception as e:
    raise ValueError(f"An error occurred: {str(e)}")
  
  return {
    "user_id": user.get("id"),
    "full_name": user.get("name"),
    "email": user.get("email"),
    "difficulty_level": user.get("difficulty_level"),
    "recent_avg_res_time": user.get("recent_avg_res_time"),
    "recent_avg_score": user.get("recent_avg_score")
  }