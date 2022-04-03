from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages 

# Create your views here.


class registrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')


    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        context = {
            'fieldvalues' : request.POST
        }

        if not User.objects.filter(username=username, email=email).exists():
            if len(password)<6:
                messages.error(request,'Password is too short')
                return render(request, 'authentication/register.html',context)
            user = User.objects.create_user(username=username, email=email)
            user.set_password(password)
            user.save()
            messages.success(request,'Account created successfully')
            return render(request, 'authentication/register.html')

        #messages.success(request, 'Registration successful')
        #messages.warning(request, 'Registration warning')
        #messages.info(request, 'Registration info')
        #messages.error(request, 'Registration error')#}
        return render(request, 'authentication/register.html')


class usernameValidationView(View):
    def post(self, request):
        data=json.loads(request.body)
        username = data['username']

        if not str(username).isalnum(): 
            return JsonResponse({'username_error': 'username should only contain alphanumeric characters'},status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'username already in use'},status=409)
        return JsonResponse({'username_valid': True})

class emailValidationView(View):
    def post(self, request):
        data=json.loads(request.body)
        email = data['email']

        if not validate_email(email): 
            return JsonResponse({'email_error': 'email is invalid'},status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'email already in use by another account.'},status=409)
        return JsonResponse({'email_valid': True})


