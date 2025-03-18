from database.db import get_db
from database.db import init_db

def find_user_by_id_demo(user_id):
  users = [
      {"id": 1, "name": "John Doe", "email": "john@example.com", "age": 25, "difficulty_level": 0},
      {"id": 2, "name": "Jane Smith", "email": "jane@example.com", "age": 30, "difficulty_level": 1},
      {"id": 3, "name": "Bob Johnson", "email": "bob@example.com", "age": 35, "difficulty_level": 2}
    ]
  try:
    # Iterate through the list to find matching ID
    for user in users:
      if str(user.get('id')) == str(user_id):  # Convert to string for comparison
        return user
    return None  # Return None if user not found
    
  except Exception as e:
    print(f"An error occurred: {str(e)}")
    return None

def find_user_by_id(user_id):
    """Fetch a user by ID from Firestore."""
    db = get_db()
    user_ref = db.collection('users-c').document(str(user_id))
    user = user_ref.get()

    if user.exists:
        return user.to_dict()  # Convert Firestore document to Python dictionary
    else:
        return None  # Return None if user not found
