from django.urls import path
from modules.social_auth.views import HomeView, LinkedInView, FacebookView, TwitterView, LinkedInProfile, LinkedInPost

from modules.social_auth.google_contact_views import GoogleContacts

from modules.social_auth.mscontactsviews import ImportContactsView, MicrosoftAuthView, Logout


app_name = 'social_auth'

urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('twitter/', TwitterView.as_view(), name='twitter'),
    path('facebook/', FacebookView.as_view(), name='facebook'),
    path('linkedin/', LinkedInView.as_view(), name='linkedin'),
    path('profile/', LinkedInProfile.as_view(), name='profile'),
    path('linkedin_post/', LinkedInPost.as_view(), name='post'),


    # Path for displaying the user information and contacts from google API.
    path('google_contacts/', GoogleContacts.as_view(), name='google_contacts'),

    path('import_contacts/', ImportContactsView.as_view(), name='import_contacts'),
    path('import_contacts/microsoft_auth/', MicrosoftAuthView.as_view(), name='microsoft_auth'),
    path('logout/', Logout.as_view(), name='logout'),

]
