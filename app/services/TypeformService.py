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
        return None, None, None
    response_data = response.json()
    return response_data, response_data.get("id"), response_data["_links"]["display"]

def get_all_forms():
    access_token = os.getenv('TYPEFORM_ACCESS_TOKEN')
    url = "https://api.typeform.com/forms"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve forms: {response.status_code}, {response.text}")
        return []
    return response.json().get('items', [])

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

def aggregate_responses_by_email():
    forms = get_all_forms()
    email_to_responses = {}
    for form in forms:
        form_id = form['id']
        responses = get_responses_by_email(form_id, None)  # Fetch all responses for the form
        if responses and 'items' in responses:
            for response in responses['items']:
                # Initialize a variable to hold the email address
                email = None
                # Iterate through each answer in the 'answers' list
                for answer in response['answers']:
                    # Check if the answer is an email field; this assumes 'email' is the field type or identifier
                    if answer['type'] == 'email':  
                        email = answer['email']
                        break
                # If an email was found, append the response to the dictionary
                if email:
                    if email in email_to_responses:
                        email_to_responses[email].append(response)
                    else:
                        email_to_responses[email] = [response]
    return email_to_responses

# Example usage:
email_responses = aggregate_responses_by_email()
print(email_responses)





#response = create_form()
#print(response)