import argparse
from googleapiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools

class GoogleFormService:
    def __init__(self):
        SCOPES = [
            "https://www.googleapis.com/auth/forms",
            "https://www.googleapis.com/auth/forms.responses.readonly",
            "https://www.googleapis.com/auth/drive"
        ]
        DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"


        # http%3A%2F%2Flocalhost
        # https://accounts.google.com/o/oauth2/auth?client_id=598513432398-prkba2149fhao9p85pcg34vevklf84lg.apps.googleusercontent.com&redirect_uri=http%3A%2F%2Flocalhost&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fforms+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fforms.responses.readonly&access_type=offline&response_type=code
        # http://localhost/?code=4/0ATx3LY4qqCmpSk2ty5f8_EUpH9MenGMwj9eqysujQzaHTnJfysOLUnMl5mvlBY-senkDtQ&scope=https://www.googleapis.com/auth/forms.responses.readonly%20https://www.googleapis.com/auth/forms
        store = file.Storage('token.json')
        creds = store.get()
        if not creds or creds.invalid or True:
            client.OOB_CALLBACK_URN = 'http://localhost'
            flow = client.flow_from_clientsecrets('client-cred.json', SCOPES)
            flow.redirect_uri="http://localhost"
            print(flow.client_secret)
            print(flow)
            parser = argparse.ArgumentParser(parents=[tools.argparser])
            flags = parser.parse_args(['--noauth_local_webserver'])
            creds = tools.run_flow(flow, store, flags)

        self.form_service = discovery.build(
            'forms', 'v1', http=creds.authorize(Http()),
            discoveryServiceUrl=DISCOVERY_DOC, static_discovery=False
        )

    def create_form(self):
        NEW_FORM = {"info": {"title": "Sample Form"}}
        result = self.form_service.forms().create(body=NEW_FORM).execute()
        print("Form created successfully!")
        return result["responderUri"]

    def get_form_responses(self, form_url):
        form_id = form_url.split("/d/")[1].split("/")[0]
        # https://docs.google.com/forms/d/1bJbUOIIp9bwZESDI1iLyvwUsV0HzeXv10oLFNP7ykTo/edit
        form_id='1bJbUOIIp9bwZESDI1iLyvwUsV0HzeXv10oLFNP7ykTo'
        responses = self.form_service.forms().responses().list(formId=form_id).execute()
        print("Responses retrieved successfully!")
        return responses

def main():
    form_service = GoogleFormService()
    form_url = form_service.create_form()
    #print("Form URL:", form_url)
    #input("Press Enter after you fill out the form...")
    responses = form_service.get_form_responses(form_url)
   # print("Form Responses:", responses)

if __name__ == "__main__":
    main()
