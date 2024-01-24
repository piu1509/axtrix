from django.urls import path, reverse_lazy
from modules.frontend.account import views
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
app_name = 'account'

urlpatterns = [
    path('login/', views.UserLogin.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='admindashboard:adminhome'), name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="account/password_reset_form.html",
                                                                email_template_name = 'account/password_reset_email.html',
                                                                success_url=reverse_lazy('account:password_reset_done')), 
    name = 'password_reset'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="account/password_reset_done.html"), 
    name = 'password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name="account/password_reset_confirm.html",success_url=reverse_lazy('account:password_reset_complete')), 
    name = 'password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="account/password_reset_complete.html"), 
    name = 'password_reset_complete')
]
