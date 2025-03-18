from pydantic import BaseModel

class ResQuestionSession(BaseModel):
  session_id: str
  user_id: int
  difficulty_level: int
  questions: list
