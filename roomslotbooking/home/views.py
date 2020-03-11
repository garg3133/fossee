from datetime import datetime, date, timedelta
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
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
            rooms_context1 += str(rooms.rooms)
    else:
        rooms_context1 = "Not yet updated!"

    # Time Slots
    time_slots_list = []
    time_slot_dict = {}
    time_slots = TimeSlot.objects.all().order_by('start_time')
    for time_slot in time_slots:
        if time_slot.end_date is None:
            time_slot_dict['id'] = time_slot.id
            time_slot_dict['start_time'] = str(time_slot.start_time)
            time_slot_dict['end_time'] = str(time_slot.end_time)
            time_slot_dict['delete'] = 'yes'
            if time_slot.start_date > today_date:
                time_slot_dict['remark'] = '(From ' + str(time_slot.start_date) + ')'
            else:
                time_slot_dict['remark'] = ''
            time_slots_list.append(time_slot_dict.copy())
        elif time_slot.end_date >= today_date and time_slot.start_date <= time_slot.end_date:
            time_slot_dict['id'] = time_slot.id
            time_slot_dict['start_time'] = str(time_slot.start_time)
            time_slot_dict['end_time'] = str(time_slot.end_time)
            time_slot_dict['delete'] = 'no'
            time_slot_dict['remark'] = '(Upto ' + str(time_slot.end_date) + ')'
            time_slots_list.append(time_slot_dict.copy())

    context = {
        'allowance' : allowance,
        'rooms_context1' : rooms_context1,
        'rooms_context2' : rooms_context2,
        'time_slots_list' : time_slots_list,
    }

    # To check overlaping of time slots
    def time_overlaps(start_time1, end_time1, start_time2, end_time2):
        if (start_time1 > start_time2 and start_time1 <end_time2) or (end_time1 > start_time2 and end_time1 <end_time2) or (start_time1 < start_time2 and end_time1 > end_time2):
            return True
        else:
            return False

    # Handling Form Data from Templates
    if request.method == 'POST':
        if request.POST.get('submit') == 'book-room':
            booking_date_str = request.POST['booked-on']
            booking_room = request.POST['booking-room']
            booking_time_slot_id = request.POST['booking-time-slot']

            booking_date = datetime.strptime(booking_date_str, '%Y-%m-%d').date()
            booking_time_slot = TimeSlot.objects.get(pk=booking_time_slot_id)
            room_manager = RoomManager.objects.filter(tenure_end=None)[0]

            booking_obj = Booking(customer=request.user, date=booking_date, room=booking_room, time_slot=booking_time_slot, room_manager=room_manager)
            booking_obj.save()

            return HttpResponseRedirect('/')

        elif request.POST.get('submit') == 'allowance':
            new_allowance_days = request.POST['allowance']
            if int(new_allowance_days) < 0:
                context1 = {
                    'allowance_error' : "Please enter a valid Pre-Booking Allowance!",
                }
                context.update(context1)
                return render(request, 'home/dashboard.html', context)
            old_allowance = PreBookingAllowance.objects.filter(end_date=None)
            if old_allowance.exists():
                old_allowance = old_allowance[0]
                old_allowance.end_date = datetime_now
                old_allowance.save()

            new_allowance = PreBookingAllowance(days=new_allowance_days)
            new_allowance.save()

            return HttpResponseRedirect('/dashboard')

        elif request.POST.get('submit') == 'rooms':
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

        elif request.POST.get('submit') == 'time_slot':
            new_start_time_str = request.POST['start_time']
            new_end_time_str = request.POST['end_time']

            new_start_time = datetime.strptime(new_start_time_str, '%H:%M').time()
            new_end_time = datetime.strptime(new_end_time_str, '%H:%M').time()

            if new_end_time <= new_start_time:
                context1 = {
                    'time_slot_error' : "Please select a valid time slot.",
                }
                context.update(context1)
                return render(request, 'home/dashboard.html', context)

            # last_booking = Booking.objects.filter(cancelled=False).order_by('-date')
            # if last_booking.exists():
            #     last_booking = last_booking[0]
            #     last_booking_date = last_booking.date
            #     new_time_slot_start_date = last_booking_date + timedelta(days=1)
            # else:
            #     new_time_slot_start_date = today_date + timedelta(days=1)

            del_time_slots_list = []  # Time Slots to be deleted
            overlapped_time_slots_list = []  # Other overlapped time slots (need not to be deleted)
            overlapped_time_slot_dict = {}
            time_slots = TimeSlot.objects.all().order_by('start_time')
            for time_slot in time_slots:
                if time_slot.end_date is None:
                    if time_overlaps(new_start_time, new_end_time, time_slot.start_time, time_slot.end_time):
                        overlapped_time_slot_dict['start_time'] = str(time_slot.start_time)
                        overlapped_time_slot_dict['end_time'] = str(time_slot.end_time)
                        if time_slot.start_date > today_date:
                            overlapped_time_slot_dict['remark'] = '(From ' + str(time_slot.start_date) + ')'
                        else:
                            overlapped_time_slot_dict['remark'] = ''
                        del_time_slots_list.append(overlapped_time_slot_dict.copy())
                elif time_slot.end_date >= today_date and time_slot.start_date <= time_slot.end_date:
                    if time_overlaps(new_start_time, new_end_time, time_slot.start_time, time_slot.end_time):
                        # overlapped_time_slot_dict['start_time'] = str(time_slot.start_time)
                        # overlapped_time_slot_dict['end_time'] = str(time_slot.end_time)
                        # overlapped_time_slot_dict['remark'] = '(Upto ' + str(time_slot.end_date) + ')'
                        overlapped_time_slots_list.append(time_slot)

            if len(del_time_slots_list) > 0:
                # Ask for deleting those time slots
                context1 = {
                    'del_time_slots_list' : del_time_slots_list,
                    'entered_start_time' : new_start_time_str,
                    'entered_end_time' : new_end_time_str,
                }
                context.update(context1)
                return render(request, 'home/dashboard.html', context)
            elif len(overlapped_time_slots_list) > 0:
                # Find max end date of overlaps
                max_end_date = today_date
                for time_slot in overlapped_time_slots_list:
                    if time_slot.end_date > max_end_date:
                        max_end_date = time_slot.end_date

                new_start_date = max_end_date + timedelta(days=1)

                new_time_slot = TimeSlot(start_time=new_start_time, end_time=new_end_time, start_date=new_start_date)
                new_time_slot.save()
                return HttpResponseRedirect('/')

            else:
                new_time_slot = TimeSlot(start_time=new_start_time, end_time=new_end_time, start_date=today_date)
                new_time_slot.save()
                return HttpResponseRedirect('/')

        elif request.POST.get('submit') == 'del_ts':
            new_start_time_str = request.POST['start_time']
            new_end_time_str = request.POST['end_time']

            # Time from form converted to datetime.time object
            new_start_time = datetime.strptime(new_start_time_str, '%H:%M').time()
            new_end_time = datetime.strptime(new_end_time_str, '%H:%M').time()

            max_end_date = today_date
            del_time_slots_list = []  # Time Slots to be deleted
            time_slots = TimeSlot.objects.all().order_by('start_time')
            for time_slot in time_slots:
                if time_slot.end_date is None:   # Time Slots to be deleted if overlaping
                    if time_overlaps(new_start_time, new_end_time, time_slot.start_time, time_slot.end_time):
                        del_time_slots_list.append(time_slot)

                        booking = Booking.objects.filter(cancelled=False, time_slot=time_slot).order_by('-date')
                        if booking.exists() and (booking[0].date > max_end_date):
                            max_end_date = booking[0].date

                elif time_slot.end_date >= today_date and time_slot.start_date <= time_slot.end_date:   # Other possible overlapping Time Slots (already deleted)
                    if time_overlaps(new_start_time, new_end_time, time_slot.start_time, time_slot.end_time):
                        # overlapped_time_slots_list.append(time_slot)
                        if time_slot.end_date > max_end_date:
                            max_end_date = time_slot.end_date

            # Deleting the overlapped time slots from the day next to max_end_date
            if len(del_time_slots_list) > 0:
                for time_slot in del_time_slots_list:
                    time_slot.end_date = max_end_date
                    time_slot.save()

            # Creating the new time slot
            new_start_date = max_end_date + timedelta(days=1)

            new_time_slot = TimeSlot(start_time=new_start_time, end_time=new_end_time, start_date=new_start_date)
            new_time_slot.save()
            return HttpResponseRedirect('/')

    return render(request, 'home/dashboard.html', context)

def deleteTimeSlot(request, uid):
    time_slot = TimeSlot.objects.get(pk=uid)

    if time_slot.end_date is None:
        end_date = date.today()
        booking = Booking.objects.filter(cancelled=False, time_slot=time_slot).order_by('-date')
        if booking.exists() and (booking[0].date > end_date):
            end_date = booking[0].date
        
        time_slot.end_date = end_date
        time_slot.save()

    return redirect('dashboard')

def bookingDateChangedAJAX(request):
    booking_date_str = request.GET.get('booking_date', None)
    booking_date = datetime.strptime(booking_date_str, '%Y-%m-%d').date()

    data = {}
    today_date = date.today()

    data['error'] = ''

    if booking_date < today_date:
        data['error'] = "*Please enter a valid date."
        return JsonResponse(data)

    # Pre-Booking Allowance Check
    days_diff = (booking_date - today_date).days
    allowance = PreBookingAllowance.objects.filter(end_date=None)
    if allowance.exists() and days_diff > allowance[0].days:
        data['error'] = "*You can only book for " + str(allowance[0].days) + " days in advance!"
        return JsonResponse(data)

    # Available Rooms
    room_obj = Rooms.objects.filter(end_date=None)
    if not room_obj.exists():
        data['error'] = "*The number of Rooms available are not defined by the Room Manager yet!"
        return JsonResponse(data)

    room_obj = room_obj[0]
    if room_obj.start_date <= booking_date:
        available_rooms = room_obj.rooms
    else:
        end_date = room_obj.start_date - timedelta(days=1)
        room_objs = Rooms.objects.filter(end_date=end_date)
        for room_obj in room_objs:
            if room_obj.start_date <= room_obj.end_time:  # Room object is valid
                available_rooms = room_obj.rooms
                break
    data['rooms'] = available_rooms
    return JsonResponse(data)

def bookingRoomChangedAJAX(request):
    booking_room = request.GET.get('booking_room', None)
    booking_date_str = request.GET.get('booking_date', None)
    booking_date = datetime.strptime(booking_date_str, '%Y-%m-%d').date()

    data = {}
    time_now = datetime.now().time()

    data['error'] = ''

    if booking_room == '':
        data['time_slots'] = []
        return JsonResponse(data)

    available_time_slots = []
    time_slot_dict = {}
    time_slots = TimeSlot.objects.all()
    for time_slot in time_slots:
        if time_slot.start_time >= time_now and time_slot.start_date <= booking_date and (time_slot.end_date is None or time_slot.end_date >= booking_date):
            if not Booking.objects.filter(cancelled=False, date=booking_date, room=booking_room, time_slot=time_slot).exists(): 
                time_slot_dict['id'] = time_slot.id
                time_slot_dict['slot'] = str(time_slot.start_time) + ' - ' + str(time_slot.end_time)
                available_time_slots.append(time_slot_dict.copy())

    if len(available_time_slots) == 0:
        data['error'] = "*No Time Slots are free for the chosen Date and Room."
    else:
        data['time_slots'] = available_time_slots

    return JsonResponse(data)


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