import os
import numpy as np
import pickle
from ..models.state import State
from ..models.difficulty import Difficulty

# Define the Q-table path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
Q_TABLE_PATH = os.path.join(BASE_DIR, "rl_model", "q_table_v1.pkl")

# Load the Q-table
with open(Q_TABLE_PATH, "rb") as f:
    Q_table = pickle.load(f)

def get_adjusted_difficulty(state: State) -> Difficulty:
    """
    Determines the new difficulty level based on user performance using Q-learning.
    """
    avg_score = round(state.avg_score, 1)
    avg_res_time = max(10, min(120, int(round(state.avg_res_time))))
    current_difficulty = state.current_difficulty

    input_state = (avg_score, avg_res_time, current_difficulty)

    # Ensure state exists in Q-table; otherwise, use a safe fallback
    if input_state in Q_table:
        action = np.argmax(Q_table[input_state]) + 1  # Convert index to action (1-based)
    else:
        # Default action: Maintain difficulty if state is unseen
        action = 2  

    # Additional checks for extreme response times
    if avg_res_time >= 50 and avg_score < 0.5:  # Too slow & struggling → Decrease difficulty
        action = 3
    elif avg_res_time <= 20 and avg_score > 0.7:  # Too fast & good score → Increase difficulty
        action = 1

    # Adjust difficulty level
    new_difficulty = current_difficulty
    if action == 1 and current_difficulty < 2:
        new_difficulty += 1
    elif action == 3 and current_difficulty > 0:
        new_difficulty -= 1

    return Difficulty(input_state=input_state, action_taken=action, adjusted_difficulty=new_difficulty)
