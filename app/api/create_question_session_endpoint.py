from fastapi import APIRouter, HTTPException
from ..utils.create_question_session import create_question_session
from ..models.req_question_session import ReqQuestionSession
from ..models.res_question_session import ResQuestionSession

router = APIRouter()

@router.post("/create-question-session", response_model=ResQuestionSession)
async def create_question_session_endpoint(request: ReqQuestionSession):
  """
  Endpoint to create a question session with 10 questions:
  - 9 standard questions
  - 1 article question
  """
  try:
    question_session = await create_question_session(user_id=request.user_id)
    return question_session
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))