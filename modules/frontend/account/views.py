import os
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from django.views import View
from django.urls import reverse_lazy
from modules.frontend.account.forms import SignUpForm


class MyView(View):
    """
    Home page view
    """

    def get(self, request):
        """
        Function to render home page
        """
        return render(request, 'account/hello.html')


class UserLogin(LoginView):
    """
    LoginView which by default provides us with a form
    """
    template_name = 'account/login.html'
    def get_success_url(self):
        return reverse_lazy('axhome:home_page')


class SignUpView(CreateView):
    """
    Created SignupView which has SignUpForm for user registraion
    """
    form_class = SignUpForm
    success_url = reverse_lazy('account:login')
    template_name = 'account/signup.html'

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(SignUpView, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('account:login')
        return super(SignUpView, self).get(*args, **kwargs)
