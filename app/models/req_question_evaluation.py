from pydantic import BaseModel

class ReqQuestionEvaluation(BaseModel):
  session_id: str
  user_id: int
  difficulty_level: int
  questions: list
  total_time: float
