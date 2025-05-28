import pytest
from unittest.mock import patch, MagicMock
from app.utils.evaluate_question_session import evaluate_session, ResQuestionEvaluation

@pytest.fixture
def sample_questions():
    return [
        {
            "question": "What is the capital of France?",
            "category": "memory_recall",
            "user_answer": "Paris",
            "correct_answer": "Paris"
        },
        {
            "question": "What comes after 5 in counting?",
            "category": "problem_solving",
            "user_answer": "6",
            "correct_answer": "6"
        }
    ]

@patch("app.utils.evaluate_question_session.model.generate_content")
@patch("app.utils.evaluate_question_session.update_difficulty_level")
def test_evaluate_session(mock_update_difficulty, mock_generate_content, sample_questions):
    # Mock Gemini response
    mock_response = MagicMock()
    mock_response.candidates[0].content.parts[0].text = """
    ```json
    {
        "question": "What is the capital of France?",
        "category": "memory_recall",
        "user_answer": "Paris",
        "correct_answer": "Paris",
        "score": 1.0,
        "correct": true
    }
    ```
    """
    mock_generate_content.return_value = mock_response

    result: ResQuestionEvaluation = evaluate_session(
        session_id="sess123",
        user_id=1,
        difficulty_level=1,
        questions=sample_questions,
        total_time=40.0
    )

    # Validate response object
    assert isinstance(result, ResQuestionEvaluation)
    assert result.session_id == "sess123"
    assert result.user_id == 1
    assert len(result.evaluations) == 2
    assert result.avg_score == 1.0  # Based on mocked 1.0 scores
    assert result.avg_time == 20.0

    mock_update_difficulty.assert_called_once()
