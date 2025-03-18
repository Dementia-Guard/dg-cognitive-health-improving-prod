import google.generativeai as genai
from fastapi import HTTPException
import random
import json
import re 

API_KEY = "AIzaSyCeuz9MBQzwAwwHJkZmtpoXxIE1q1RAjeA"  # Replace with your Gemini API key
MODEL_NAME = "gemini-2.0-flash"

def generate_standard_question(difficulty_level: int, category: str) -> dict:
    """Generates a cognitive exercise question using Gemini API."""
    try:
        # Configure API
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel(MODEL_NAME)

        # Define categories
        categories = ["memory_recall", "object_recall", "date_questions", "backward_count", "problem_solving"]
        category = category.lower()

        prompts = {
            "memory_recall": f"""
            Generate a unique cognitive exercise question to test **memory recall**, following **MMSE and MoCA standards**.  
            - **Dynamically generate three different words** each time based on the specified difficulty level:  
                - **0**: Everyday objects (e.g., "banana", "table", "ball")  
                - **1**: Moderately complex words (e.g., "parrot", "lantern", "puzzle")  
                - **2**: Uncommon or abstract words (e.g., "telescope", "barometer", "metronome")  
            -requested difficulty level is {difficulty_level}

            - Ensure that the words **change with each generation** to prevent repetition.  

            Return only **valid JSON**, with **no additional text or formatting**.  

            {{
                "question": "Listen carefully: I will say three words, and later I will ask you to recall them. The words are:",
                "sub_question": "What were the three words I mentioned earlier?",
                "words": ["<unique_word1>", "<unique_word2>", "<unique_word3>"],
                "correct_answer": ["<unique_word1>", "<unique_word2>", "<unique_word3>"]
            }}
            """,

            "object_recall": f"""
            Generate a unique cognitive exercise question to test **object recognition and recall**, following **MMSE and MoCA standards**.  
            - The participant must identify an object from an image.  
            - **Ensure that each generated object is different** from previous outputs by using randomness in selection.  

            - The difficulty level affects the **complexity of the object**:  
                - **0**: Common objects (e.g., "apple", "pen", "hat")  
                - **1**: Moderately complex objects (e.g., "telescope", "chessboard", "sewing machine")  
                - **2**: Uncommon or abstract objects (e.g., "astrolabe", "sundial", "anemometer")  
            -requested difficulty level is {difficulty_level}

            - Generate an appropriate **public domain image link** based on the object.  

            Return only **valid JSON**, with **no additional text or formatting**.  

            {{
                "question": "Can you name this object?",
                "answers": ["<Randomized Option 1>", "<Randomized Option 2>", "<Randomized Option 3>", "<Randomized Option 4>"],
                "correct_answer": "<Correct Answer>",
                "link_of_img": "https://pixabay.com/api/?key=49349511-20b9eb3c76f0e2f4c37783c91&q=<random_unique_object>&image_type=photo"
            }}
            """,

            "date_questions": f"""
            Generate a fresh, unique cognitive exercise question testing **date and time awareness**, based on **MMSE and MoCA standards**.  
            - Each question must be **different from previous ones**, ensuring variety.  

            - The difficulty level determines the complexity:  
                - **0**: Basic date awareness (e.g., "What day of the week is today?")  
                - **1**: Specific date-related (e.g., "What is today's full date?")  
                - **2**: Complex reasoning (e.g., "If today is Monday, what date was last Wednesday?")  
            -requested difficulty level is {difficulty_level}

            Return only **valid JSON**, with **no additional text or formatting**.  

            {{
                "question": "<Dynamically Generated Date Question>",
                "answers": ["<Random Option 1>", "<Random Option 2>", "<Random Option 3>", "<Random Option 4>"],
                "correct_answer": "<Correct Answer>"
            }}
            """,

            "backward_count": f"""
            Generate a **new backward counting task** for each request, ensuring **non-repetitive numbers**.  
            - The task assesses **attention and numerical ability** according to **MMSE and MoCA standards**.  

            - The difficulty level determines the **starting number**:  
                - **0**: Start between **0-10** (e.g., "Count backward from 7")  
                - **1**: Start between **10-20** (e.g., "Count backward from 15")  
                - **2**: Start between **20-50** (e.g., "Count backward from 37")  
            -requested difficulty level is {difficulty_level}

            - Ensure each generated question uses **a different starting number**.  

            Return only **valid JSON**, with **no additional text or formatting**.  

            {{
                "question": "Count backward from <random_starting_number>.",
                "answers": [<random_num1>, <random_num2>, <random_num3>, <random_num4>]
            }}
            """,

            "problem_solving": f"""
            Generate a **unique problem-solving cognitive exercise question**, following **MMSE and MoCA standards**.  
            - Each generated question must be **different from previous ones**.  
            - Ensure **cultural relevance** by using Sri Lankan references (e.g., local currency Rs., local items).  

            - The difficulty level determines complexity:  
                - **0**: Simple problems (e.g., "If you buy 3 mangoes and eat 1, how many do you have?")  
                - **1**: Moderate logic (e.g., "What is the next number in the pattern: 5, 10, 15, __?")  
                - **2**: Advanced reasoning (e.g., "If a train leaves Colombo at 2:00 PM and arrives in Kandy at 6:00 PM, how long was the journey?")  
            -requested difficulty level is {difficulty_level}

            - Ensure that numbers and objects **change dynamically** with each generation.  

            Return only **valid JSON**, with **no additional text or formatting**.  

            {{
                "question": "<Dynamically Generated Problem-Solving Question>",
                "answers": ["<Random Option 1>", "<Random Option 2>", "<Random Option 3>", "<Random Option 4>"],
                "correct_answer": "<Correct Answer>"
            }}
            """

        }


        prompt = prompts[category]

        response = model.generate_content(prompt)

        # 🔥 Extract text safely
        if not response or not hasattr(response, "candidates"):
            raise ValueError("Invalid response from Gemini API.")

        generated_text = response.candidates[0].content.parts[0].text.strip()

        # 🔥 Remove Markdown formatting (```json ... ```)
        cleaned_text = re.sub(r"```json\s*|\s*```", "", generated_text).strip()

        # 🔥 Ensure valid JSON
        try:
            data = json.loads(cleaned_text)  # ✅ Parse the cleaned JSON response
        except json.JSONDecodeError:
            raise ValueError(f"Failed to parse cleaned Gemini response: {cleaned_text}")

        # 🔥 Validate and normalize the response structure
        if not isinstance(data, dict) or "question" not in data:
            raise ValueError(f"Response does not contain the required fields: {cleaned_text}")

        # Handle category-specific response structures
        if category == "memory_recall":
            if "sub_question" not in data or "words" not in data:
                raise ValueError(f"Memory recall response missing required fields: {cleaned_text}")
            return {
                "question": data["question"],
                "sub_question": data["sub_question"],
                "possible_answers": data["correct_answer"],  # Treat words as possible answers
                "words": data["words"],
                "category": category,
            }
        elif category == "backward_count":
            if "answers" not in data:
                raise ValueError(f"Response missing required fields for {category}: {cleaned_text}")
            return {
                "question": data["question"],
                "possible_answers": data["answers"],
                "category": category,
            }
        else:
            if "answers" not in data:
                raise ValueError(f"Response missing required fields for {category}: {cleaned_text}")
            result = {
                "question": data["question"],
                "possible_answers": data["answers"],
                "correct_answer": data["correct_answer"],
                "category": category,
            }
            # Add link_of_img for object_recall category
            if category == "object_recall" and "link_of_img" in data:
                result["link_of_img"] = data["link_of_img"]
            return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate question with Gemini: {e}")
