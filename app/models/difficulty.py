from pydantic import BaseModel
from typing import Tuple

class Difficulty(BaseModel):
    input_state: Tuple[float, int, int]
    action_taken: int
    adjusted_difficulty: int
