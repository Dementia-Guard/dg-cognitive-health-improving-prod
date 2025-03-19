from pydantic import BaseModel
from typing import Tuple

class Difficulty(BaseModel):
    input_state: Tuple[float, float, int]
    action_taken: int
    adjusted_difficulty: int
