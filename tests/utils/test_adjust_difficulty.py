import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from app.models.state import State
from app.utils.difficulty_adjust import get_adjusted_difficulty
from app.models.difficulty import Difficulty

# Mock the Q_table inside adjust_difficulty before import (use monkeypatch)
@pytest.fixture(autouse=True)
def mock_q_table(monkeypatch):
    mock_table = {
        (0.5, 60, 1): [0.1, 0.3, 0.6],
        (0.8, 15, 1): [0.7, 0.2, 0.1],
        (0.3, 90, 1): [0.2, 0.1, 0.7],
    }

    monkeypatch.setattr("app.utils.difficulty_adjust.Q_table", mock_table)

def test_increase_difficulty():
    state = State(avg_score=0.8, avg_res_time=15, current_difficulty=1)
    result: Difficulty = get_adjusted_difficulty(state)
    assert result.adjusted_difficulty == 2
    assert result.action_taken == 1

def test_decrease_difficulty():
    state = State(avg_score=0.3, avg_res_time=90, current_difficulty=1)
    result: Difficulty = get_adjusted_difficulty(state)
    assert result.adjusted_difficulty == 0
    assert result.action_taken == 3

def test_maintain_difficulty_for_unseen_state():
    state = State(avg_score=0.6, avg_res_time=40, current_difficulty=1)
    result: Difficulty = get_adjusted_difficulty(state)
    assert result.adjusted_difficulty == 1  # Maintain difficulty
    assert result.action_taken == 2

def test_extreme_low_score_high_time_forced_decrease():
    state = State(avg_score=0.2, avg_res_time=60, current_difficulty=1)
    result: Difficulty = get_adjusted_difficulty(state)
    assert result.adjusted_difficulty == 0
    assert result.action_taken == 3

def test_extreme_high_score_low_time_forced_increase():
    state = State(avg_score=0.9, avg_res_time=15, current_difficulty=0)
    result: Difficulty = get_adjusted_difficulty(state)
    assert result.adjusted_difficulty == 1
    assert result.action_taken == 1
