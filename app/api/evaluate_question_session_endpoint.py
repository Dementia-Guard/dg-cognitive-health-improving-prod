from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..utils.evaluate_question_session import evaluate_session

router = APIRouter()

class ReqQuestionEvaluation(BaseModel):
    session_id: str
    user_id: int
    difficulty_level: int
    questions: list
    total_time: float

class ResQuestionEvaluation(BaseModel):
    session_id: str
    user_id: int
    difficulty_level: int
    evaluations: list
    avg_score: float
    avg_time: float

@router.post("/evaluate-session", response_model=ResQuestionEvaluation)
async def evaluate_question_session_endpoint(request: ReqQuestionEvaluation):
    try:
        # Call the evaluation function
        result = evaluate_session(
            session_id=request.session_id,
            user_id=request.user_id,
            difficulty_level=request.difficulty_level,
            questions=request.questions,
            total_time=request.total_time
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Evaluation failed: {str(e)}")