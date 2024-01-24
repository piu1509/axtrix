import msal
import requests

from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response

from decouple import config
import os

client_id1 = config('MS_CLIENT_ID')
redirect_uri1 = config('MS_REDIRECT_URL')
client_secret1 =  config('MS_CLIENT_SECRET')


class ImportContactsView(APIView):
    """
    APIView for importing contact details of a Microsoft Account.
    """
    def get(self, request):
        # Set up the MSAL ConfidentialClientApplication instance
        client_id = client_id1
        client_secret = client_secret1
        authority = 'https://login.microsoftonline.com/common'
        app = msal.ConfidentialClientApplication(
            client_id=client_id,
            client_credential=client_secret,
            authority=authority,
        )

        if 'access_token' not in request.session:

            # If the code parameter is in the query string, use it to acquire an access token
            if 'code' in request.GET:
                code = request.GET['code']
                scopes = ['https://graph.microsoft.com/Contacts.Read']
                redirect_uri = redirect_uri1
                result = app.acquire_token_by_authorization_code(code, scopes=scopes, redirect_uri=redirect_uri)
                if 'access_token' in result:
                    request.session['access_token'] = result['access_token']

            # If the code parameter is not in the query string, redirect the user to the Microsoft login page
            else:
                authorize_url = app.get_authorization_request_url(
                    scopes=['https://graph.microsoft.com/Contacts.Read'],
                    redirect_uri= redirect_uri1,
                    response_mode='query',
                )
                return HttpResponseRedirect(authorize_url)
            
        graph_url = 'https://graph.microsoft.com/v1.0/me'
        headers = {'Authorization': 'Bearer ' + request.session['access_token']}
        response = requests.get(graph_url, headers=headers)
        
        if response.status_code == 200:
            
            profile = {}
            profile['name' ] = response.json()['displayName']
            profile['mobilePhone' ] = response.json()['mobilePhone']
            profile['userPrincipalName' ] = response.json()['userPrincipalName']

        # Use the access token to make a GET request to the contacts endpoint
        graph_url = 'https://graph.microsoft.com/v1.0/me/contacts'
        headers = {'Authorization': 'Bearer ' + request.session['access_token']}
        response = requests.get(graph_url, headers=headers)
        if response.status_code == 200:
            contacts = response.json()['value']

            short_contacts = [{'displayName': c['displayName'], 'mobilePhone': c['mobilePhone'], 'givenName': c['givenName'], 'surname': c['surname'], 'emailAddresses': c['emailAddresses']}
                for c in contacts]

            return Response({'profile':profile,'contacts': short_contacts})
        else:
            return Response({'error': 'Unable to retrieve contacts from Microsoft API'})        


class MicrosoftAuthView(APIView):
    """
    APIView for authenticating users.
    """
    def get(self, request):
        # Set up the MSAL ConfidentialClientApplication instance
        client_id = client_id1
        client_secret = client_secret1
        authority = 'https://login.microsoftonline.com/common'
        app = msal.ConfidentialClientApplication(
            client_id=client_id, 
            client_credential=client_secret,
            authority=authority,
        )

        # Get an authorization URL for the Microsoft Graph API
        redirect_uri = redirect_uri1
        scopes = ['https://graph.microsoft.com/contacts.read', 'User.Read']
        auth_url = app.get_authorization_request_url(
            scopes=scopes, 
            redirect_uri=redirect_uri1,
        )

        # Redirect the user to the Microsoft authentication page
        return redirect(auth_url)

    def post(self, request):
        # Exchange the authorization code for an access token
        client_id = client_id1
        client_secret = client_secret1
        authority = 'https://login.microsoftonline.com/common'
        redirect_uri = redirect_uri1
        token_endpoint = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'
        code = request.GET.get('code')
        if not code:
            return HttpResponseBadRequest('Authorization code not found.')

        app = msal.ConfidentialClientApplication(
            client_id=client_id, 
            client_credential=client_secret,
            authority=authority,
        )
        token_request_data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': redirect_uri1,
            'client_id': client_id,
            'client_secret': client_secret,
            'scope' : ['https://graph.microsoft.com/contacts.read',]
        }
        response = requests.post(token_endpoint, data=token_request_data)
        response_data = response.json()

        if 'access_token' not in response_data:
            request.session['access_token'] = response_data['access_token']

            return HttpResponseBadRequest('Failed to obtain access token.')

        # Save the access token to the user's session or database
        access_token = response_data['access_token']
        request.session['access_token'] = access_token

        # Redirect the user to the desired page
        return redirect('import_contacts')


class Logout(APIView):
    """
    To logout a user.
    """
    def get(self, request):
        request.session.flush()
        if os.path.exists('token.json'):
            os.remove('token.json')
        return redirect('social_auth:home')
