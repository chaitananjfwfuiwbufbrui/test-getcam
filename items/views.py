from django.shortcuts import render
from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.
from django.shortcuts import render
from math import ceil
import json
import  datetime
# Create your views here.
from django.shortcuts import render,HttpResponse,redirect
from items.models import *
from  django.contrib.auth.models import User 
from django.contrib.auth import logout,authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from  django.contrib import messages


from datetime import datetime ,timedelta,date
# Create your views here.
def login(request):
    if request.method == 'POST':
       loginuser = request.POST['loginuser'] 
       loginPassword= request.POST['loginPassword']
       user = authenticate(username=loginuser,password=loginPassword)
       if user is not None:
            auth_login(request,user)
            messages.success(request,"sucessfully login")
            
            return redirect('home')
       else:
           messages.error(request,'invalid username')
           return redirect('login')
  
    return render(request,'login.html')
def logouts(request):
    logout(request)
    messages.success(request,'successfully logout')
    return redirect('home')
    



def signin(request):
    if request.method == 'POST':
       user = request.POST['signupuser'] 
       email = request.POST['signupemail']
       signupfname = request.POST['signupfname']
       signupsname = request.POST['signupsname']
       pass1 = request.POST['inputPassword1']
       pass2 = request.POST['inputPassword2']
       if len(user) > 10:
            messages.error(request,"user name should be less than 10 characters")
            return redirect('home')
            
       if pass1 != pass2:
            messages.error(request,"passwoard should be match")
            return redirect('home')

       if not user.isalnum():
            messages.error(request,"username must be in alphabhates and numaric")
            return redirect('home')



       myuser = User.objects.create_user(user,email,pass1)
       myuser.first_name= signupfname
       myuser.last_name = signupsname
       myuser.save()
       messages.success(request,"your account has been successfully created")
       create_cus = Customer.objects.get_or_create(user=user,name=signupfname,email=email)
       create_cus.save()
       return redirect('signin')
       
    else:
        return render(request,'signinpage.html')  

       

