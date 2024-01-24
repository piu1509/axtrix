from django.urls import path
from modules.frontend.axhome import views

app_name = 'axhome'

urlpatterns = [
	path('', views.HomePageView.as_view(), name='home_page'),
    path('about/', views.AboutPageView.as_view(), name='about_page'),
    path('contact/', views.ContactPageView.as_view(), name='contact_page')
]