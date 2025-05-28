import google.generativeai as genai
import json
from pydantic import BaseModel
from typing import List, Dict, Any
import time
from ..utils.difficulty_adjust import get_adjusted_difficulty
from ..models.state import State
from ..services.user_services import update_difficulty_level

API_KEY = "AIzaSyC9DA3LBilEzHGxkUY5D-bbyMgnhaLaScA"
MODEL_NAME = "gemini-2.5-flash-preview-05-20"

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(MODEL_NAME)

class ResQuestionEvaluation(BaseModel):
    session_id: str
    user_id: int
    difficulty_level: int
    evaluations: list
    avg_score: float
    avg_time: float

def evaluate_single_question(question: Dict[str, Any]) -> Dict[str, Any]:
    """Evaluate a single question using Gemini AI"""
    try:
        # Prepare prompt for Gemini
        prompt = f"""
        Evaluate the following question response and return a JSON object with score (0-1) and evaluation details:
        
        Question Data:
        {json.dumps(question, indent=2)}
        
        Rules:
        - For memory_recall: Check if user_answer matches with the all words in correct_answer exactly. (case-insensitive) If user answer is not order in correct_answer, score 0.5, correct true
        - For object_recall/problem_solving: Check if user_answer matches correct_answer exactly if answer match with similar word in correct_answer, score 0.5, correct true
        - For problem_solving: Check if user_answer matches correct_answer exactly (case-insensitive)
        - For date_questions: Check if user_answer correct using your kowledge. consider the current real world time, date, weeks, etc. when finding the correct answer
        - For backward_count: Check if user_answer matches the correct sequence
        - For article: Determine the correct answer from the article and check if user_answer correct
        - Score 1 for correct, 0 for incorrect
        - If question is correct, correct need to be true else it need to be false
        
        Return only valid JSON with:
        {{
            "question": "Question text",
            "category": "Category name",
            "user_answer": "<use_answer>",
            "correct_answer": "<correct_answer>",
            "score": 0.0 to 1.0,
            "correct": true or false,
        }}
        """
        
        response = model.generate_content(prompt)
        
        # Extract and clean response
        generated_text = response.candidates[0].content.parts[0].text.strip()
        cleaned_text = generated_text.replace("```json", "").replace("```", "").strip()
        
        evaluation_result = json.loads(cleaned_text)
        print(evaluation_result)
        
        # Ensure required fields are present
        if not all(key in evaluation_result for key in ["score", "correct"]):
            raise ValueError("Invalid evaluation response from Gemini")
            
        # Add original question details to result
        return {
            "question": question["question"],
            "category": question["category"],
            "user_answer": evaluation_result["user_answer"],
            "correct_answer": evaluation_result["correct_answer"],
            "score": evaluation_result["score"],
            "correct": evaluation_result["correct"]
        }
        
    except Exception as e:
        return {
            "question": question["question"],
            "category": question["category"],
            "user_answer": question["user_answer"],
            "correct_answer": question.get("correct_answer", ""),
            "score": 0.0,
            "correct": False
        }

def evaluate_session(session_id: str, user_id: int, difficulty_level: int, questions: List[Dict[str, Any]], total_time:float) -> ResQuestionEvaluation:
    """Evaluate an entire question session"""
    evaluations = []
    total_score = 0.0
    
    # Evaluate each question
    for question in questions:
        # print(json.dumps(question, indent=2))
        print(f"Evaluating question: {question['question']}, user answer: {question['user_answer']}", flush=True)
        evaluation = evaluate_single_question(question)
        evaluations.append(evaluation)
        total_score += evaluation["score"]
    
    # Calculate averages
    num_questions = len(questions)
    avg_score = total_score / num_questions if num_questions > 0 else 0.0
    avg_time = total_time / num_questions if num_questions > 0 else 0.0

    state = State(
        avg_score=avg_score,
        avg_res_time=avg_time,
        current_difficulty=difficulty_level
    )

    difficulty = get_adjusted_difficulty(state)
    print(f"Adjusted difficulty: {difficulty}", flush=True)

    adjusted_difficulty = difficulty.adjusted_difficulty
    action_taken = difficulty.action_taken

    try:
        update_difficulty_level(user_id, adjusted_difficulty, avg_score, avg_time, action_taken)
    except Exception as e:
        print(f"An error occurred while updating difficulty level: {str(e)}", flush=True)
    
    # Return response model
    return ResQuestionEvaluation(
        session_id=session_id,
        user_id=user_id,
        difficulty_level=difficulty_level,
        evaluations=evaluations,
        avg_score=avg_score,
        avg_time=avg_time
    )

