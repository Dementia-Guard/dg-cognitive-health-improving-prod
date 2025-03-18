import requests

def generate_article_question(difficulty_level: int):
  # API endpoint URL
  url = "https://dg-article-exercises-7az7elfqqa-as.a.run.app/generate_question"
  
  # Request body
  payload = {"difficulty_level": difficulty_level}
  headers = {
    "Content-Type": "application/json",
    "User-Agent": "PostmanRuntime/7.36.0"  # Mimic Postman's user agent
  }

  print(f"URL: {url}")
  print(f"Headers: {headers}")
  print(f"Payload: {payload}")
  
  try:
    response = requests.post(url, json=payload, headers=headers, timeout=30)
    response.raise_for_status()
    print(f"Response Status: {response.status_code}")
    print(f"Response Text: {response.text}")
    return response.json()
  except requests.exceptions.HTTPError as e:
    print(f"HTTP Error: {e}")
    print(f"Response Text: {response.text}")
    return None
  except requests.exceptions.RequestException as e:
    print(f"General Error: {e}")
    return None