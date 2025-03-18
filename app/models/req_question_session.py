from pydantic import BaseModel

class ReqQuestionSession(BaseModel):
  user_id: int
