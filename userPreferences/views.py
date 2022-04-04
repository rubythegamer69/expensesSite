from locale import currency
from turtle import pd
from django.shortcuts import render
import os
import json
from django.conf import settings
import pdb
from .models import userPreferences
from django.contrib import messages
# Create your views here.

def index(request):
    currency_data = []
    file_path = os.path.join(settings.BASE_DIR,'currencies.json')
    with open(file_path,'r') as json_file:
        data = json.load(json_file)
        for i,j in data.items():
            currency_data.append({'name': i,'value': j})  
    exists = user_preference = userPreferences.objects.filter(user=request.user).exists()
    user_preference = None
    
    if exists:
        user_preference = userPreferences.objects.get(user=request.user)
    if request.method == 'GET':
            #pdb.set_trace()
        return render(request, 'preferences/index.html',{'currencies': currency_data, 'user_preference':user_preference})
    else:
        currency= request.POST['currency']
        if exists:
            user_preference.currency= currency
            user_preference.save()
        else:
            userPreferences.objects.create(user=request.user, currency=currency) 
        messages.success(request,'changes applied successfully')
        return render(request, 'preferences/index.html',{'currencies': currency_data, 'user_preference':user_preference})

    