from pydantic import BaseModel

class State(BaseModel):
  avg_score: float
  avg_res_time: float
  current_difficulty: int
