from pydantic import BaseModel

class ResQuestionEvaluation(BaseModel):
  session_id: str
  user_id: int
  difficulty_level: int
  evaluations: list
  avg_score: float
  avg_time: float
