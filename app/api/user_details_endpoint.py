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
            raise HTTPException(status_code=404, detail="User not found")

        # Prepare the response dictionary
        response = {
            "user_id": user.get("user_id"),
            "full_name": user.get("full_name"),
            "email": user.get("email"),
            "difficulty_level": user.get("difficulty_level"),
            "recent_avg_res_time": user.get("recent_avg_res_time"),
            "recent_avg_score": user.get("recent_avg_score")
        }

        # Check for None values in required fields
        required_fields = ["user_id", "full_name", "email", "difficulty_level", "recent_avg_res_time", "recent_avg_score"]
        missing_fields = [field for field in required_fields if response[field] is None]
        if missing_fields:
            raise HTTPException(
                status_code=500,
                detail=f"User data is incomplete. Missing or invalid fields: {', '.join(missing_fields)}"
            )

        return response

    except HTTPException as e:
        raise e  # Re-raise HTTPException for FastAPI to handle
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")