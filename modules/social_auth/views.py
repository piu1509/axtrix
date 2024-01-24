import requests
import tweepy
import io

from io import BytesIO
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from rest_framework import status
from rest_framework.response import Response
from decouple import config

client_id = config('CLIENT_ID')
redirect_uri = config('REDIRECT_URL')
client_secret =  config('CLIENT_SECRET')

consumer_key1 = config('CONSUMER_KEY')
consumer_secret1 = config('CONSUMER_SECRET')
access_token1 =  config('ACCESS_TOKEN')
access_token_secret1 = config('ACCESS_TOKEN_SECRET')

page_id1 = config('PAGE_ID')
page_access_token1 = config('PAGE_ACCESS_TOKEN')


class HomeView(View):
    def get(self, request):
        api_url = "https://www.linkedin.com/oauth/v2"
        params = {
        'response_type': 'code',
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'scope': 'r_liteprofile,r_emailaddress,w_member_social'
        }
        response = requests.get(f'{api_url}/authorization', params=params)
        return render(request, 'social_home.html', {'url': response.url})


class TwitterView(View):
    def get(self, request):
        return render(request, 'twitter.html')
    
    def post(self, request, *args, **kwargs):

        consumer_key = consumer_key1
        consumer_secret = consumer_secret1
        access_token = access_token1
        access_token_secret = access_token_secret1

        auth = tweepy.auth.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        api = tweepy.API(auth)

        tweet_text = request.POST.get('message')
        image = request.FILES.get('image')

        file_bytes = BytesIO(image.read())

        try:
            if 'image' in request.FILES:
                # Upload the image to Twitter
                media = api.media_upload(filename=image.name, file=file_bytes)

                # Include the media ID in the tweet
                api.update_status(status=tweet_text, media_ids=[media.media_id])

            else:
                # No image was uploaded, tweet only the text
                api.update_status(status=tweet_text)
            
            return redirect('social_auth:home')
        except tweepy.TweepyException as e:
            error_message = f'Error publishing post: {str(e)}'
            return render(request, 'twitter.html', {'error_message': error_message})


class FacebookView(View):
    def get(self, request):
        return render(request, 'fb.html')

    def post(self, request):
        # Get message and image from form data
        message = request.POST.get('message')
        image = request.FILES.get('image')
        if not image:
            error_message = 'Please select an image'
            return render(request, 'fb.html', {'error_message': error_message})

        # Set up variables
        page_id = page_id1
        page_access_token = page_access_token1

        # Convert image to bytes and create file-like object
        image_bytes = BytesIO(image.read())
        image_file = ('image.jpg', image_bytes, 'image/jpeg')

        # Create post
        post_data = {'message': message}
        post_files = {'source': image_file}
        post_headers = {'Authorization': 'Bearer ' + page_access_token}
        post_response = requests.post(f'https://graph.facebook.com/{page_id}/photos', data=post_data, files=post_files, headers=post_headers)

        # Check if post was successful
        if post_response.status_code == 200:
            return redirect('social_auth:home')
        else:
            error_message = 'Error publishing post: ' + post_response.text
            return render(request, 'fb.html', {'error_message': error_message})


class LinkedInView(View):
    def get(self, request):
        api_url = "https://www.linkedin.com/oauth/v2"
        params = {
        'response_type': 'code',
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'scope': 'r_liteprofile,r_emailaddress,w_member_social'
        }
        response = requests.get(f'{api_url}/authorization', params=params)

        return render(request, 'login.html', {'url': response.url})


class LinkedInProfile(View):
    def get(self, request):
        code = request.GET.get('code', None)
        code = code

        payload = f'client_id={client_id}&client_secret={client_secret}&redirect_uri={redirect_uri}&code={code}'
        api_url = "https://www.linkedin.com/oauth/v2/accessToken"

        api = f'https://www.linkedin.com/oauth/v2/accessToken?code={code}&grant_type=authorization_code&client_id={client_id}&client_secret={client_secret}&redirect_uri={redirect_uri}'
        response = requests.get(api)
        data = response.json()
        request.session['access_token'] = data['access_token']
        
        access_token = request.session['access_token']
        headers = {'Authorization': f'Bearer {access_token}',
        'cache-control': 'no-cache',
        'X-Restli-Protocol-Version': '2.0.0'
        }
        response = requests.get('https://api.linkedin.com/v2/me', headers=headers)
        user_info = response.json()
        request.session['user_id'] = user_info['id']
        return render(request, 'userprofile.html', {'user_info': user_info})


class LinkedInPost(View):
    def get(self, request):
        api_url = 'https://api.linkedin.com/v2/ugcPosts'
        message = 'Preparing a LinkedIn Bot -1'
        urn = request.session['user_id']
        author = f'urn:li:person:{urn}'
        access_token = request.session['access_token']
        headers = {'Authorization': f'Bearer {access_token}',
        'cache-control': 'no-cache',
        'X-Restli-Protocol-Version': '2.0.0'
        }

        message = '''
        Interested to automate LinkedIn using #Python and the LinkedIn API?
        Read this in-depth Python for #SEO post I wrote.
        '''
        link = 'https://www.jcchouinard.com/how-to-use-the-linkedin-api-python/'
        link_text = 'Complete tutorial using the LinkedIn API'

        post_data = {
        "author": author,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
        "com.linkedin.ugc.ShareContent": {
        "shareCommentary": {
        "text": message
        },
        "shareMediaCategory": "ARTICLE",
        "media": [
        {
        "status": "READY",
        "description": {
        "text": message
        },
        "originalUrl": link,
        "title": {
        "text": link_text
        }
        }
        ]
        }
        },
        "visibility": {
        "com.linkedin.ugc.MemberNetworkVisibility": "CONNECTIONS"
        }
        }
        r = requests.post(api_url, headers=headers, json=post_data)
        return redirect('social_auth:home')


