from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import (
    Profile,
)

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        # return redirect('dashboard')
        return redirect('dashboard')

    if request.method == 'POST':
        if request.POST.get('submit') == 'login':
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                context = {
                    'login_error' : "Invalid Username or Password",
                }
                return render(request, 'home/index.html', context)

        elif request.POST.get('submit') == 'signup':
            username = request.POST['username']
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            error = ''
            obj = User.objects.filter(username=username)
            if obj.exists():
                error = "Account with entered username already exists"
                return render(request, "home/index.html", {'signup_error' : error})
            if password1 and password2 and password1 != password2:
                error = "Passwords don't match"
                return render(request, "home/index.html", {'signup_error' : error})
            
            obj = User(username = username)
            obj.set_password(password1)
            obj.save()

            user = authenticate(username=username, password=password1)
            login(request, user)
            return redirect('dashboard')

    return render(request, 'home/index.html')

def dashboard(request):
    if not request.user.is_authenticated:
        return render(request, 'home/index.html')

    if not Profile.objects.filter(user=request.user).exists():
        return redirect('setprofile')
    return render(request, 'home/dashboard.html')

def setprofile(request):
    if request.user.is_authenticated:
        if Profile.objects.filter(user=request.user).exists():
            return redirect('dashboard')
        if request.method == 'POST':
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            gender  = request.POST['gender']
            contact_no = request.POST['contact_no']
            address = request.POST['address']

            # Updating User Model
            user_obj = request.user
            user_obj.email = email
            user_obj.first_name = first_name
            user_obj.last_name = last_name
            user_obj.save()

            # Updating Profile Model
            profile_obj = Profile( user=user_obj, gender=gender, contact_no=contact_no, address=address)
            profile_obj.save()

            return redirect('dashboard')

        return render(request, 'home/setprofile.html')

    return redirect('home')