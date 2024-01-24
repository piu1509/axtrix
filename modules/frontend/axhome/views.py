from django.shortcuts import render
from django.views import View


class HomePageView(View):
	"""
	Class based view which renders Home page.
	"""
	def get(self, request):
		return render(request, 'home.html')


class AboutPageView(View):
	"""
	Class based view which renders About Us page.
	"""
	def get(self, request):
		return render(request, 'about_us.html')


class ContactPageView(View):
	"""
	Class based view which renders Contact Us page.
	"""
	def get(self, request):
		return render(request, 'contact_us.html')
