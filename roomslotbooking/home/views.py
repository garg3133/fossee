from datetime import datetime, date, timedelta
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import (
    Profile,
    RoomManager,
    Rooms,
    TimeSlot,
    PreBookingAllowance,
    Booking,
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

    # Global Variables
    today_date = date.today()
    datetime_now = datetime.now()

    # Info to be sent all the time

    # Pre-Booking Allowance
    allowance = PreBookingAllowance.objects.filter(end_date=None)
    if allowance.exists():
        allowance = allowance[0]
        # if allowance.start_date == datetime_now:
        #     allowance = PreBookingAllowance.objects.filter(end_date)
    else:
        allowance = "Not yet updated!"

    # Rooms
    rooms_context1 = ''
    rooms_context2 = ''
    rooms = Rooms.objects.filter(end_date=None)
    if rooms.exists():
        rooms = rooms[0]
        # rooms_context += str(rooms.rooms)
        if rooms.start_date > today_date:
            rooms_old = Rooms.objects.filter(end_date=rooms.start_date-timedelta(days=1))
            if rooms_old.exists():
                rooms_old = rooms_old[0]
                rooms_context1 += str(rooms_old.rooms) + ' (Upto ' + str(rooms_old.end_date) + ')'
                rooms_context2 += str(rooms.rooms) + ' (From ' + str(rooms.start_date) + ')'
        else:
            rooms_context1 += str(rooms_old.rooms)
    else:
        rooms_context1 = "Not yet updated!"

    context = {
        'allowance' : allowance,
        'rooms_context1' : rooms_context1,
        'rooms_context2' : rooms_context2,
    }

    if request.method == 'POST':
        if request.POST.get('submit') == 'allowance':
            new_allowance_days = request.POST['allowance']
            old_allowance = PreBookingAllowance.objects.filter(end_date=None)
            if old_allowance.exists():
                old_allowance = old_allowance[0]
                old_allowance.end_date = datetime_now
                old_allowance.save()

            new_allowance = PreBookingAllowance(days=new_allowance_days)
            new_allowance.save()

            return HttpResponseRedirect('/dashboard')

        if request.POST.get('submit') == 'rooms':
            new_rooms = request.POST['rooms']
            last_booking = Booking.objects.filter(cancelled=False).order_by('-date')
            if last_booking.exists():
                last_booking = last_booking[0]
                last_booking_date = last_booking.date

                # Change end_date of older instance of Rooms
                old_rooms_obj = Rooms.objects.filter(end_date=None)
                if old_rooms_obj.exists():
                    old_rooms_obj = old_rooms_obj[0]
                    old_rooms_obj.end_date = last_booking_date
                    old_rooms_obj.save()
                # Create new instance of Rooms
                new_rooms_start_date = last_booking_date + timedelta(days=1)
                rooms_obj = Rooms(rooms=new_rooms, start_date=new_rooms_start_date)
                rooms_obj.save()
            else:
                # Change end_date of older instance of Rooms
                old_rooms_obj = Rooms.objects.filter(end_date=None)
                if old_rooms_obj.exists():
                    old_rooms_obj = old_rooms_obj[0]
                    old_rooms_obj.end_date = today_date
                    old_rooms_obj.save()
                    new_rooms_start_date = today_date + timedelta(days=1)
                else:
                    new_rooms_start_date = today_date

                # Create new instance of Rooms
                rooms_obj = Rooms(rooms=new_rooms, start_date=new_rooms_start_date)
                rooms_obj.save()

            return HttpResponseRedirect('/dashboard')


    return render(request, 'home/dashboard.html', context)

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