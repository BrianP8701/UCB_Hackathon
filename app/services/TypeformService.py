import os
import requests
from dotenv import load_dotenv

load_dotenv()

def create_form():
    access_token = os.getenv('TYPEFORM_ACCESS_TOKEN')
    url = "https://api.typeform.com/forms"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    data = {
        "title": "User Feedback Form",
        "fields": [
            {
                "type": "multiple_choice",
                "title": "What is your least hated programming language?",
                "properties": {
                    "choices": [
                        {"label": "Python"},
                        {"label": "Java"},
                        {"label": "C++"},
                        {"label": "JavaScript"}
                    ]
                }
            },
            {
                "type": "long_text",
                "title": "Please provide feedback on our tool:",
                "properties": {
                    "description": "Your feedback is valuable to us."
                }
            },
            {
                "type": "email",
                "title": "What is your email address?",
                "properties": {
                    "description": "Your feedback is valuable to us."
                }
            }
        ]
    }
    response = requests.post(url, headers=headers, json=data) 
    if response.status_code != 201:
        print(f"Failed to create form: {response.status_code}, {response.text}")
        return None, None
    response_data = response.json()
    return response_data, response_data.get("id")

def get_responses_by_email(form_id, user_email):
    access_token = os.getenv('TYPEFORM_ACCESS_TOKEN')
    if not form_id:
        print("Invalid form ID. Cannot fetch responses.")
        return None
    url = f"https://api.typeform.com/forms/{form_id}/responses"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"query": user_email}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        print(f"Failed to retrieve responses: {response.status_code}, {response.text}")
        return None
    return response.json()



response = create_form()
print(response)