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

            - **Dynamically generate three different words** each time based on the specified difficulty level {difficulty_level}:
                - **0 (Easy)**: Common everyday objects.
                - **1 (Moderate)**: Slightly less common but familiar words.
                - **2 (Challenging)**: Words that are less frequently used but still recognizable.
            
            - **Ensure that words change with each generation** to prevent repetition.

            - **The words should be familiar to elderly users** while still being appropriately challenging at higher levels.

            - **Output must be valid JSON**, with **no additional text or formatting**.

            {{
                "question": "Listen carefully: I will say three words, and later I will ask you to recall them. The words are:",
                "sub_question": "What were the three words I mentioned earlier?",
                "words": ["<unique_word1>", "<unique_word2>", "<unique_word3>"],
                "correct_answer": ["<unique_word1>", "<unique_word2>", "<unique_word3>"],
            }}

            """,

            "object_recall": f"""
            Generate a unique cognitive exercise question to test **object recognition and recall**, following **MMSE and MoCA standards**.

            - The participant must **identify an object from an image**.  

            - **Ensure that each generated object is different** from previous outputs by using randomness in selection.  

            - Requested difficulty level is {difficulty_level}.

            - **The difficulty level affects the complexity of the object**:  
                - **0 (Easy)**: Very common, simple objects found in daily life.  
                - **1 (Moderate)**: Slightly more complex but still familiar objects.  
                - **2 (Challenging)**: Common but less frequently mentioned objects.  

            - **Objects must**:  
                - Be universally recognizable and not specific to any profession, culture, or region.  
                - Be physical objects that can be **seen and touched** (e.g., avoid abstract concepts like "justice" or "freedom").  
                - Not include highly specialized or scientific terms that a general audience would not recognize.  

            - **Generate an appropriate** **public domain image link** based on the object. The image should be a **vector illustration**.  

            - Return only **valid JSON**, with **no additional text or formatting**.

            {{
                "question": "Can you name this object?",
                "answers": ["<Randomized Option 1>", "<Randomized Option 2>", "<Randomized Option 3>", "<Randomized Option 4>"],
                "correct_answer": "<Correct Answer>",
                "link_of_img": "https://pixabay.com/api/?key=49349511-20b9eb3c76f0e2f4c37783c91&q=<random_unique_object>&image_type=vector",
            }}

            """,

            "date_questions": f"""
            Generate a **unique** cognitive exercise question testing **date and time awareness**, based on **MMSE and MoCA standards**.

            - **Each generated question must be different from previous ones**, ensuring variety.
            - The question **must be contextually relevant** to the current date/time.

            - Requested difficulty level is {difficulty_level}.

            - **The difficulty level determines the complexity**:  
                - **0 (Easy)**: Basic date awareness.  
                - **1 (Moderate)**: Specific date-related questions.  
                - **2 (Challenging)**: Requires logical reasoning.  

            - **Correct answers must be dynamically generated** based on the real-time date.  
            - **Avoid generic questions like ‘What is the current year?’** unless relevant to difficulty.  
            - **Ensure that all answer choices are reasonable and not obviously incorrect.**  

            - Return only **valid JSON**, with **no additional text or formatting**.

            {{
                "question": "<Dynamically Generated Date Question>",
                "answers": ["<Randomized Answer 1>", "<Randomized Answer 2>", "<Randomized Answer 3>", "<Randomized Answer 4>"],
                "correct_answer": "<Correct Answer Based on Real Date>",
            }}
            """,

            "backward_count": f"""
            Generate a **new backward counting task** for each request, ensuring **non-repetitive numbers**.

            - The task assesses **attention and numerical ability** according to **MMSE and MoCA standards**.
            - Each question must be **different from previous ones**, ensuring variety.

            - Requested difficulty level is {difficulty_level}.

            - **Difficulty level determines the starting number**:
                - **0 (Easy)**: Start between 4-19 (e.g., "Count four numbers backward starting from 7").
                - **1 (Moderate)**: Start between 20-40 (e.g., "Count five numbers backward starting from 15").
                - **2 (Challenging)**: Start between 41-70 (e.g., "Count six numbers backward starting from 37").

            - The **number of steps to count backward** must match the **length of the answers array**.
            - Ensure **each generated question uses a different starting number** within the difficulty range.
            - **Must not generate negative numbers** (when reaching 0, it should be the last number).
            - If the backward count reaches **0 before completing the required steps**, adjust the starting number accordingly.
            
            Return only **valid JSON**, with **no additional text or formatting**.

            {{
                "question": "Count <length_of_answer_array> numbers backward from <random_starting_number>.",
                "answers": [<start_number>, <next_number>, <next_number>, ..., <last_number>]
            }}
            """,

            "problem_solving": f"""
            Generate a **unique problem-solving cognitive exercise question**, following **MMSE and MoCA standards**.

            - Each generated question must be **different from previous ones**, ensuring variety.
            - Ensure **cultural relevance** by using **Sri Lankan references** (e.g., currency Rs., local transportation, familiar items like tea, coconuts, mangoes).
            - Use **clear and concise wording** to ensure the question is understandable for all participants.

            - Requested difficulty level is {difficulty_level}.

            - **Difficulty level determines complexity**:
                - **0 (Easy)**: Basic arithmetic or logical reasoning (e.g., "If you buy 3 mangoes and eat 1, how many do you have left?")
                - **1 (Moderate)**: Pattern recognition or practical calculations (e.g., "What is the next number in the pattern: 5, 10, 15, __?")
                - **2 (Challenging but manageable)**: Time calculations or real-world problem-solving (e.g., "A train leaves Colombo at 2:00 PM and arrives in Kandy at 6:00 PM. How long was the journey?").

            - Ensure that **numbers and objects change dynamically** with each generation.
            - **Avoid making questions too complex or requiring advanced math knowledge** beyond basic logic and reasoning.
            - **Do not use abstract concepts** that may confuse participants.

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
