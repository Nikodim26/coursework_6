from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.views.decorators.cache import cache_page
from django.views.generic import RedirectView

from config.settings import CACHE_TIMEOUT
from users.apps import UsersConfig
from users.forms import UserLoginForm
from users.views import UserCreateView, email_verification, HomeView, IntermediateView, UsersListView

app_name = UsersConfig.name

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='users:login', permanent=False), name='root'),
    path('login/', LoginView.as_view(template_name='login_register.html', form_class=UserLoginForm), name='login'),
    path('login_/', IntermediateView.as_view(), name='login_'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', UserCreateView.as_view(), name='register'),
    path("email-confirm/<str:token>/", email_verification, name='email-confirm'),
    path('home/', HomeView.as_view(), name='home'),
    path('users/', cache_page(CACHE_TIMEOUT)(UsersListView.as_view()), name='users'),

]
