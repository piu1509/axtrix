from django.http import HttpResponse
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from rest_framework.response import Response
from rest_framework.views import APIView

SCOPES = ['https://www.googleapis.com/auth/contacts.readonly','https://www.googleapis.com/auth/userinfo.email','https://www.googleapis.com/auth/userinfo.profile','openid']


class GoogleContacts(APIView):
    """
        Fetches and displays all the contacts from google account using people API.
    """
    def get(self, request, *args, **kwargs):
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)      
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                'modules/social_auth/credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        try:
            user_info_service = build(
                'oauth2', 'v2', credentials=creds)
            user_info = user_info_service.userinfo().get().execute()
            email = user_info.get('email')
            username = user_info.get('name')
            picture = user_info.get('picture')  

            people_service = build('people', 'v1', credentials=creds)
            result = people_service.people().connections().list(resourceName='people/me', personFields='names,emailAddresses,phoneNumbers').execute()            
            connections = result.get('connections', [])
            contact_list = []
            user_dict = {
                            'username':username,
                            'user-email':email,
                            'picture':picture
                        }
            for people in connections:
                names = people.get('names')
                contact_numbers = people.get('phoneNumbers')
                if names:
                    name = names[0].get('displayName')
                    name_dict = {'name':name}                
                if contact_numbers:
                    contact_number = contact_numbers[0].get('value')
                    name_dict['contact_number'] = contact_number
                    contact_list.append(name_dict)
            return Response({"user-info":user_dict, "contact_list":contact_list})
        except HttpError as error:
            return HttpResponse(error)
