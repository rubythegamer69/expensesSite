from .views import emailValidationView,loginView,logoutView, verificationView, registrationView, usernameValidationView
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

urlpatterns =[
    path('register',registrationView.as_view(),name='register'),
    path('validate-username',csrf_exempt(usernameValidationView.as_view()),name='validate-username'),
    path('validate-email',csrf_exempt(emailValidationView.as_view()),	name='validate-email'),
    path('activate/<uidb64><token>', verificationView.as_view(),name =  "activate"),
    path('login', loginView.as_view(),name = "login"),
    path('logout', logoutView.as_view(),name = "logout"),
    ]