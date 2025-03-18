import firebase_admin
from firebase_admin import credentials, firestore
import os
import json
from dotenv import load_dotenv

load_dotenv()

# Initialize Firebase Admin SDK
if not firebase_admin._apps:  # Prevent re-initialization
    # Option 1: Load from FIREBASE_SERVICE_ACCOUNT_KEY (JSON string) - used in Cloud Run/GitHub workflow
    service_account_json = os.getenv("FIREBASE_SERVICE_ACCOUNT_KEY")
    if service_account_json:
        try:
            cred_dict = json.loads(service_account_json)
            cred = credentials.Certificate(cred_dict)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid FIREBASE_SERVICE_ACCOUNT_KEY JSON: {e}")
    # Option 3: Fallback to Application Default Credentials - for Cloud Run with service account or gcloud auth
    else:
        cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred)

db = firestore.client()

def get_db():
    """Return the Firestore client."""
    return db

def init_db():
    """Initialize Firestore with sample data."""
    
    users_ref = db.collection('users-c')
    if not users_ref.limit(1).get():
        # Insert sample users
        users_ref.document('1').set({
            'user_id': 1,
            'full_name': 'Michael Johnson',
            'birth_date': '1965-04-10',
            'hometown': 'Springfield, Illinois',
            'difficulty_level': 0,
            'email': 'michael.johnson@example.com',
            'recent_avg_res_time': 45,
            'recent_avg_score': 0.75,
            'previous_sessions': [
                {
                    'session_id': 'nsasik1',
                    'avg_res_time': 50,
                    'avg_score': 0.2,
                    'current_difficulty_level': 1,
                    'adjusted_difficulty_level': 0
                }
            ]
        })
        
        users_ref.document('2').set({
            'user_id': 2,
            'full_name': 'Sarah Williams',
            'birth_date': '1970-07-15',
            'hometown': 'Austin, Texas',
            'difficulty_level': 1,
            'email': 'sarah.williams@example.com',
            'recent_avg_res_time': 38,
            'recent_avg_score': 0.85,
            'previous_sessions': [
                {
                    'session_id': 'nsasik2',
                    'avg_res_time': 42,
                    'avg_score': 0.4,
                    'current_difficulty_level': 1,
                    'adjusted_difficulty_level': 1
                }
            ]
        })
        
        users_ref.document('3').set({
            'user_id': 3,
            'full_name': 'David Brown',
            'birth_date': '1982-12-20',
            'hometown': 'Boston, Massachusetts',
            'difficulty_level': 2,
            'email': 'david.brown@example.com',
            'recent_avg_res_time': 52,
            'recent_avg_score': 0.6,
            'previous_sessions': [
                {
                    'session_id': 'nsasik3',
                    'avg_res_time': 55,
                    'avg_score': 0.3,
                    'current_difficulty_level': 2,
                    'adjusted_difficulty_level': 1
                }
            ]
        })
    print("Firestore initialized with sample data if empty.")
