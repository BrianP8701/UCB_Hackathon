import os
import requests
from dotenv import load_dotenv

from app.types import FormFieldType, TypeformResponse, FormField
from typing import Dict, Tuple, List

load_dotenv()

class TypeformService:
    def __init__(self):
        self.access_token = os.getenv('TYPEFORM_ACCESS_TOKEN')

    def create_form(self, typeform_schema) -> Tuple[Dict, str, str]:
        url = "https://api.typeform.com/forms"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

        response = requests.post(url, headers=headers, json=typeform_schema) 
        if response.status_code != 201:
            print(f"Failed to create form: {response.status_code}, {response.text}")
            return None, None, None
        response_data = response.json()
        return response_data, response_data.get("id"), response_data["_links"]["display"]

    def get_all_forms(self):
        url = "https://api.typeform.com/forms"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to retrieve forms: {response.status_code}, {response.text}")
            return []
        return response.json().get('items', [])

    def get_responses_by_email(self, form_id, user_email):
        if not form_id:
            print("Invalid form ID. Cannot fetch responses.")
            return None
        url = f"https://api.typeform.com/forms/{form_id}/responses"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        params = {"query": user_email}
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            print(f"Failed to retrieve responses: {response.status_code}, {response.text}")
            return None
        return response.json()


    def aggregate_responses_by_email(self):
        forms = self.get_all_forms()
        email_to_responses = {}
        for form in forms:
            form_id = form['id']
            responses = self.get_responses_by_email(form_id, None)  # Fetch all responses for the form
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


    def get_all_responses(self, form_id) -> List[TypeformResponse]:
        responses = self.get_responses_by_email(form_id, None)  # Fetch all responses for the form
        formatted_responses = []
        for response in responses['items']:  # Access the 'items' key
            response_id = response['response_id']
            answers = response['answers']
            formatted_response = TypeformResponse(
                id=response_id, 
                answers=answers
            )
            formatted_responses.append(formatted_response)
        return formatted_responses

    def build_typeform_schema(self, form_fields: List[FormField]):
        form_fields.append(
            FormField(
                id="email",
                name="Email",
                description="Enter your email address",
                form_field_type=FormFieldType.text
            )
        )
        typeform_fields = []
        for field in form_fields:
            typeform_field_type = None
            if field.form_field_type == FormFieldType.text:
                typeform_field_type = "short_text"
            elif field.form_field_type == FormFieldType.date:
                typeform_field_type = "date"
            elif field.form_field_type == FormFieldType.checkbox:
                typeform_field_type = "yes_no"

            if typeform_field_type:
                typeform_field = {
                    "title": field.name,
                    "type": typeform_field_type,
                    "ref": field.id, 
                    "properties": {
                        "description": field.description
                    }
                }
                typeform_fields.append(typeform_field)
        return {
            "title": "Generated Form",
            "fields": typeform_fields
        }





# Example usage:
# typeformService = TypeformService()

# form_fields = [
#     FormField(id="1", name="Name", description="Your full name", form_field_type=FormFieldType.text),
#     FormField(id="2", name="Birthdate", description="Your birthdate", form_field_type=FormFieldType.date),
#     FormField(id="3", name="Subscribe", description="Subscribe to newsletter", form_field_type=FormFieldType.checkbox)
# ]

# typeform_schema = typeformService.build_typeform_schema(form_fields)
# print(typeform_schema)

# response, form_id, form_url = typeformService.create_form(typeform_schema)
# print(f"Response: {response}")
# print(f"Form ID: {form_id}")
# print(f"Form URL: {form_url}")

# # Example usage:
# email_responses = aggregate_responses_by_email()
# print(email_responses)





# #response = create_form()
#print(response)