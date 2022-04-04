from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages 
from django.core.mail import EmailMessage
from django.contrib import auth
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .util import token_Generator
from django.shortcuts import redirect
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
            user.is_active= False
            user.save()

            uidb64= urlsafe_base64_encode(force_bytes(user.pk))

            domain = get_current_site(request).domain
            link = reverse('activate', kwargs={'uidb64': uidb64, 'token': token_Generator.make_token(user)})

            activation_link = 'http://'+domain+link
            email_subject = 'Activate your account'
            email_body = 'Hi ' +user.username + 'Click this link to activate your account\n' + activation_link
            
            
            email = EmailMessage(
                email_subject,
                email_body,
                'noreply@gmail.com',
                [email]
            )

            email.send(fail_silently=False)

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


class verificationView(View):
    def get(self, request, uidb64, token):
        try:
            id=force_str(urlsafe_base64_decode(uidb64))
            user= User.objects.get(pk=id)

            if not token_Generator.check_token(user,token):
                return redirect('login'+ '?message='+ 'Account already activated')

            if user.is_active:
                return redirect('login')
            user.is_active= True
            user.save()

            messages.success(request,'Account has been activated successfully')
            return redirect('login')
        except Exception as exception:
            pass
        return redirect('login')
        

class loginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')
    
    def post(self, request): 
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password: 
            user = auth.authenticate(username = username, password = password)
            if user: 
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request,'Welcome '+user.username+', login was successful')
                    return redirect('expenses')
                messages.error(request,'Login failed because account is not activated. Check your email and try again.')
                return render(request, 'authentication/login.html')        
            messages.error(request,'Login failed. invalid username or password.')
            return render(request, 'authentication/login.html')
        messages.error(request,'Please fill all fields!')
        return render(request, 'authentication/login.html')


class logoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request,'You have been logged out')
        return redirect('login')