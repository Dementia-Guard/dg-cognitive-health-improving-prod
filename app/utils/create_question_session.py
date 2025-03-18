from ..utils.generate_standard_question import generate_standard_question
from ..utils.generate_article_question import generate_article_question
from ..services.user_services import find_user_by_id
import uuid
import random

async def create_question_session(user_id) -> list:
  try:
    user = find_user_by_id(user_id)
    if user is None:
      raise ValueError("User not found")
  except Exception as e:
    raise ValueError(f"An error occurred: {str(e)}")
  
  difficulty_level = user.get('difficulty_level')

  session_id = f"S{str(uuid.uuid4())[:5]}"
  
  categories = ["memory_recall", "object_recall", "date_questions", "backward_count", "problem_solving"]
  questions = []
  for category in categories:
    question_data = generate_standard_question(difficulty_level, category)

    formatted_question = {
      "question": question_data.get("question", ""),
      "sub_question": question_data.get("sub_question", ""),
      "possible_answers": question_data.get("possible_answers", []),
      "correct_answer": question_data.get("correct_answer", ""),
      "words": question_data.get("words", []),
      "category": category,
      "link_of_img": question_data.get("link_of_img", "")
    }

    formatted_question = {k: v for k, v in formatted_question.items() if v}

    questions.append(formatted_question)
  
  try:
    article_question = generate_article_question(difficulty_level)
    print(f"Article question: {article_question}", flush=True)

    is_valid_format = False
    if article_question and "output" in article_question and article_question["output"]:
      output_text = article_question["output"][0]
      if isinstance(output_text, str) and "question: " in output_text and " answer: " in output_text:
        try:
          question_part, answer_part = output_text.split(" answer: ", 1)
          if question_part.startswith("question: "):
            is_valid_format = True
        except ValueError:
          pass
    
    if is_valid_format:
      questions.append(article_question)
    else:
      print(f"Invalid article question format detected: {article_question.get('output', 'No output')}. Generating fallback question.", flush=True)
      # Generate a fallback question from a random category
      random_category = random.choice(categories)
      fallback_question_data = generate_standard_question(difficulty_level, random_category)
      formatted_fallback_question = {
        "question": fallback_question_data.get("question", ""),
        "sub_question": fallback_question_data.get("sub_question", ""),
        "possible_answers": fallback_question_data.get("possible_answers", []),
        "correct_answer": fallback_question_data.get("correct_answer", ""),
        "words": fallback_question_data.get("words", []),
        "category": random_category,
        "link_of_img": fallback_question_data.get("link_of_img", "")
      }
      formatted_fallback_question = {k: v for k, v in formatted_fallback_question.items() if v}
      questions.append(formatted_fallback_question)
  except Exception as e:
    print(f"An error occurred while generating article question: {e}. Generating fallback question.", flush=True)
    # Generate a fallback question from a random category
    random_category = random.choice(categories)
    fallback_question_data = generate_standard_question(difficulty_level, random_category)
    formatted_fallback_question = {
      "question": fallback_question_data.get("question", ""),
      "sub_question": fallback_question_data.get("sub_question", ""),
      "possible_answers": fallback_question_data.get("possible_answers", []),
      "correct_answer": fallback_question_data.get("correct_answer", ""),
      "words": fallback_question_data.get("words", []),
      "category": random_category,
      "link_of_img": fallback_question_data.get("link_of_img", "")
    }
    formatted_fallback_question = {k: v for k, v in formatted_fallback_question.items() if v}
    questions.append(formatted_fallback_question)

  response = {
    "session_id": session_id,
    "user_id": str(user_id),
    "difficulty_level": difficulty_level,
    "questions": questions
  }
  
  return response