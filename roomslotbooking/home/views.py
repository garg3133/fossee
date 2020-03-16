from datetime import datetime, date, timedelta
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.forms.models import model_to_dict
from django.contrib import messages
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
        ''' If User is autheticated, check if User profile is complete
            If Profile is complete, redirect to setprofile
            Else redirect to dashboard
        '''
        if not Profile.objects.filter(user=request.user).exists():
            return redirect('setprofile')
        return redirect('dashboard')

    # Login and SignUp requests
    if request.method == 'POST':
        if request.POST.get('submit') == 'login':
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(username=username, password=password)
            if user is not None:
                # Correct Username and Password entered
                login(request, user)
                messages.success(request, 'Logged in successfully!')
                return redirect('dashboard')
            else:
                # Invalid Username or Password entered
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
                # Username already exists
                error = "Account with entered username already exists"
                return render(request, "home/index.html", {'signup_error' : error})
            if password1 and password2 and password1 != password2:
                # Passwords don't match
                error = "Passwords don't match"
                return render(request, "home/index.html", {'signup_error' : error})
            
            # Valid Username and Passwords entered
            obj = User(username = username)
            obj.set_password(password1)
            obj.save()

            # Authenticate and Login the User
            user = authenticate(username=username, password=password1)
            login(request, user)
            return redirect('setprofile')

    return render(request, 'home/index.html')

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('home')

    if not Profile.objects.filter(user=request.user).exists():
        return redirect('setprofile')

    # For Global Use
    today_date = date.today()
    datetime_now = datetime.now()

    # Info to be sent all the time

    # User Bookings
    user_bookings = Booking.objects.filter(customer=request.user).order_by('-booked_on')

    # All Bookings
    all_bookings = Booking.objects.all().order_by('-date', 'room', 'time_slot__start_time', 'cancelled')

    # Get Pre-Booking Allowance
    allowance = PreBookingAllowance.objects.filter(end_date=None)
    if allowance.exists():
        allowance = allowance[0]
    else:
        allowance = "Not yet updated!"

    # Get Rooms
    rooms_context1 = ''
    rooms_context2 = ''
    rooms = Rooms.objects.filter(end_date=None)
    if rooms.exists():
        rooms = rooms[0]
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

    # Get Time Slots
    time_slots_list = []
    time_slot_dict = {}
    time_slots = TimeSlot.objects.all().order_by('start_time')
    for time_slot in time_slots:
        # Non-deleted time slots
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
        # Time Slots deleted but deletion not came under effect
        elif time_slot.end_date >= today_date and time_slot.start_date <= time_slot.end_date:
            time_slot_dict['id'] = time_slot.id
            time_slot_dict['start_time'] = str(time_slot.start_time)
            time_slot_dict['end_time'] = str(time_slot.end_time)
            time_slot_dict['delete'] = 'no'
            time_slot_dict['remark'] = '(Upto ' + str(time_slot.end_date) + ')'
            time_slots_list.append(time_slot_dict.copy())

    context = {
        'user_bookings' : user_bookings,
        'all_bookings' : all_bookings,
        'allowance' : allowance,
        'rooms_context1' : rooms_context1,
        'rooms_context2' : rooms_context2,
        'time_slots_list' : time_slots_list,

        'today_date' : today_date,
        'time_now' : datetime_now.time(),
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
            # Form Data
            booking_date_str = request.POST['booked-on']
            booking_room = request.POST['booking-room']
            booking_time_slot_id = request.POST['booking-time-slot']

            # Create Booking Instance
            booking_date = datetime.strptime(booking_date_str, '%Y-%m-%d').date()
            booking_time_slot = TimeSlot.objects.get(pk=booking_time_slot_id)
            room_manager = RoomManager.objects.filter(tenure_end=None)[0]

            booking_obj = Booking(customer=request.user, date=booking_date, room=booking_room, time_slot=booking_time_slot, room_manager=room_manager)
            booking_obj.save()

            # Show Success Message on dashboard
            messages.success(request, 'Room booked successfully!')

            return HttpResponseRedirect('/dashboard/')

        elif request.POST.get('submit') == 'allowance':
            # Form Data
            new_allowance_days = request.POST['allowance']

            # Check is data is valid
            if int(new_allowance_days) < 0:
                context1 = {
                    'allowance_error' : "Please enter a valid Pre-Booking Allowance!",
                }
                context.update(context1)
                return render(request, 'home/dashboard.html', context)

            # Check if older instance of allownace exists
            old_allowance = PreBookingAllowance.objects.filter(end_date=None)

            # Close old allowance if it exists
            if old_allowance.exists():
                old_allowance = old_allowance[0]
                old_allowance.end_date = datetime_now
                old_allowance.save()

            # Create new Allowance instance
            new_allowance = PreBookingAllowance(days=new_allowance_days)
            new_allowance.save()

            # Show Success Message on dashboard
            messages.success(request, 'Pre-Booking Allowance changed successfully!')

            return HttpResponseRedirect('/dashboard/')

        elif request.POST.get('submit') == 'rooms':
            # Form Data
            new_rooms = request.POST['rooms']

            # Check is data is valid
            if int(new_rooms) < 0:
                context1 = {
                    'rooms_error' : "Please enter valid Number of Rooms!",
                }
                context.update(context1)
                return render(request, 'home/dashboard.html', context)

            # Fetch Bookings Query Set sorted by date
            bookings = Booking.objects.filter(cancelled=False).order_by('-date')

            # If bookings exists and last booking is after today
            if bookings.exists() and bookings[0].date > today_date:
                last_booking = bookings[0]
                last_booking_date = last_booking.date

                # Close older instance of Rooms
                old_rooms_obj = Rooms.objects.filter(end_date=None)
                if old_rooms_obj.exists():
                    old_rooms_obj = old_rooms_obj[0]
                    old_rooms_obj.end_date = last_booking_date
                    old_rooms_obj.save()

                # Create new instance of Rooms
                new_rooms_start_date = last_booking_date + timedelta(days=1)
                rooms_obj = Rooms(rooms=new_rooms, start_date=new_rooms_start_date)
                rooms_obj.save()

            # If no booking exists or last booking is for today or already completed
            else:
                # Close older instance of Rooms
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

            # Show Success Message on dashboard
            messages.success(request, 'Rooms updated successfully!')

            return HttpResponseRedirect('/dashboard/')

        elif request.POST.get('submit') == 'time_slot':
            # Form Data
            new_start_time_str = request.POST['start_time']
            new_end_time_str = request.POST['end_time']

            # Create Time objects from Form Data
            new_start_time = datetime.strptime(new_start_time_str, '%H:%M').time()
            new_end_time = datetime.strptime(new_end_time_str, '%H:%M').time()

            # Check if data is valid
            if new_end_time <= new_start_time:
                context1 = {
                    'time_slot_error' : "Please select a valid time slot!",
                }
                context.update(context1)
                return render(request, 'home/dashboard.html', context)

            del_time_slots_list = []  # Time Slots to be deleted
            overlapped_time_slots_list = []  # Other overlapped time slots (need not to be deleted)
            overlapped_time_slot_dict = {}  # Time Slot dictionary to be appended in above lists

            # Fetch all existing time slots
            time_slots = TimeSlot.objects.all().order_by('start_time')

            for time_slot in time_slots:
                # If time slot is not deleted
                if time_slot.end_date is None:
                    if time_overlaps(new_start_time, new_end_time, time_slot.start_time, time_slot.end_time):
                        overlapped_time_slot_dict['start_time'] = str(time_slot.start_time)
                        overlapped_time_slot_dict['end_time'] = str(time_slot.end_time)
                        if time_slot.start_date > today_date:
                            overlapped_time_slot_dict['remark'] = '(From ' + str(time_slot.start_date) + ')'
                        else:
                            overlapped_time_slot_dict['remark'] = ''
                        del_time_slots_list.append(overlapped_time_slot_dict.copy())

                # If time slot is already deleted by not yet came into effect
                elif time_slot.end_date >= today_date and time_slot.start_date <= time_slot.end_date:
                    if time_overlaps(new_start_time, new_end_time, time_slot.start_time, time_slot.end_time):
                        overlapped_time_slots_list.append(time_slot)

            # If some time slots need to be deleted
            if len(del_time_slots_list) > 0:
                # Ask for deleting those time slots
                context1 = {
                    'del_time_slots_list' : del_time_slots_list,
                    'entered_start_time' : new_start_time_str,
                    'entered_end_time' : new_end_time_str,
                }
                context.update(context1)
                return render(request, 'home/dashboard.html', context)

            # If no time slot needs to be deleted but some already deleted time slots are overlapping
            elif len(overlapped_time_slots_list) > 0:
                # Find max end date of overlaps
                max_end_date = today_date
                for time_slot in overlapped_time_slots_list:
                    if time_slot.end_date > max_end_date:
                        max_end_date = time_slot.end_date

                # New start date one day after max end date
                new_start_date = max_end_date + timedelta(days=1)

                # Create new time slot instance
                new_time_slot = TimeSlot(start_time=new_start_time, end_time=new_end_time, start_date=new_start_date)
                new_time_slot.save()

                # Show Success Message on dashboard
                messages.success(request, 'Time Slot added successfully!')

                return HttpResponseRedirect('/dashboard/')

            # If no time slot overlaps
            else:
                # Create new time slot instance
                new_time_slot = TimeSlot(start_time=new_start_time, end_time=new_end_time, start_date=today_date)
                new_time_slot.save()

                # Show Success Message on dashboard
                messages.success(request, 'Time Slot added successfully!')

                return HttpResponseRedirect('/dashboard/')

        elif request.POST.get('submit') == 'del_ts':
            # Form Data
            new_start_time_str = request.POST['start_time']
            new_end_time_str = request.POST['end_time']

            # Time from form converted to datetime.time object
            new_start_time = datetime.strptime(new_start_time_str, '%H:%M').time()
            new_end_time = datetime.strptime(new_end_time_str, '%H:%M').time()

            max_end_date = today_date  # Max end date initialized
            del_time_slots_list = []  # Time Slots to be deleted

            # Fetch all Time Slots
            time_slots = TimeSlot.objects.all().order_by('start_time')
            for time_slot in time_slots:
                # Time Slots to be deleted if overlaping
                if time_slot.end_date is None:
                    if time_overlaps(new_start_time, new_end_time, time_slot.start_time, time_slot.end_time):
                        del_time_slots_list.append(time_slot)

                        booking = Booking.objects.filter(cancelled=False, time_slot=time_slot).order_by('-date')
                        if booking.exists() and (booking[0].date > max_end_date):
                            max_end_date = booking[0].date

                # Other possible overlapping Time Slots (already deleted)
                elif time_slot.end_date >= today_date and time_slot.start_date <= time_slot.end_date:
                    if time_overlaps(new_start_time, new_end_time, time_slot.start_time, time_slot.end_time):
                        # overlapped_time_slots_list.append(time_slot)
                        if time_slot.end_date > max_end_date:
                            max_end_date = time_slot.end_date

            # Deleting the overlapped time slots from the day next to max_end_date
            if len(del_time_slots_list) > 0:
                for time_slot in del_time_slots_list:
                    time_slot.end_date = max_end_date
                    time_slot.save()

            # Creating the new time slot instance
            new_start_date = max_end_date + timedelta(days=1)

            new_time_slot = TimeSlot(start_time=new_start_time, end_time=new_end_time, start_date=new_start_date)
            new_time_slot.save()

            # Show Success Message on dashboard
            messages.success(request, 'New Time Slot added successfully!')

            return HttpResponseRedirect('/dashboard/')

        elif request.POST.get('submit') == 'update-profile':
            # Form Data
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
            profile_obj = Profile.objects.get(user=request.user)
            profile_obj.gender = gender
            profile_obj.contact_no = contact_no
            profile_obj.address = address
            profile_obj.save()

            # Show Success Message on dashboard
            messages.success(request, 'Profile updated successfully!')

            return HttpResponseRedirect('/dashboard/')

    return render(request, 'home/dashboard.html', context)

def setprofile(request):
    if request.user.is_authenticated:
        # If User Profile already exists
        if Profile.objects.filter(user=request.user).exists():
            return redirect('dashboard')

        if request.method == 'POST':
            # Form Data
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
            profile_obj = Profile(user=user_obj, gender=gender, contact_no=contact_no, address=address)
            profile_obj.save()

            return redirect('dashboard')

        return render(request, 'home/setprofile.html')

    return redirect('home')

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

def deleteBooking(request, uid):
    booking = Booking.objects.get(pk=uid)
    booking.cancelled = True
    booking.save()

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
            if room_obj.start_date <= room_obj.end_date:  # Room object is valid
                available_rooms = room_obj.rooms
                break
    data['rooms'] = available_rooms
    return JsonResponse(data)

def bookingRoomChangedAJAX(request):
    booking_room = request.GET.get('booking_room', None)
    booking_date_str = request.GET.get('booking_date', None)
    booking_date = datetime.strptime(booking_date_str, '%Y-%m-%d').date()

    data = {}
    today_date = date.today()
    time_now = datetime.now().time()

    data['error'] = ''

    if booking_room == '':
        data['time_slots'] = []
        return JsonResponse(data)

    available_time_slots = []
    time_slot_dict = {}
    time_slots = TimeSlot.objects.all().order_by('start_time')
    for time_slot in time_slots:
        # If booking date is later, all time slots are allowed but only remaining slots of day if booking is today
        if booking_date > today_date or (booking_date == today_date and time_slot.start_time >= time_now):
            # Time Slot is available on the booking day
            if time_slot.start_date <= booking_date and (time_slot.end_date is None or time_slot.end_date >= booking_date):
                if not Booking.objects.filter(cancelled=False, date=booking_date, room=booking_room, time_slot=time_slot).exists(): 
                    time_slot_dict['id'] = time_slot.id
                    time_slot_dict['slot'] = str(time_slot.start_time) + ' - ' + str(time_slot.end_time)
                    available_time_slots.append(time_slot_dict.copy())

    if len(available_time_slots) == 0:
        data['error'] = "*No Time Slots are free for the chosen Date and Room."
    else:
        data['time_slots'] = available_time_slots

    return JsonResponse(data)

def roomManagerDetailsAJAX(request):
    room_manager_id = request.GET.get('room_manager_id', None)

    room_manager = RoomManager.objects.get(pk=room_manager_id)
    
    data = {
        'first_name' : room_manager.manager.first_name,
        'last_name' : room_manager.manager.last_name,
        'email' : room_manager.manager.email,
        'contact_no' : room_manager.manager.profile.contact_no,
    }

    return JsonResponse(data)

def customerDetailsAJAX(request):
    customer_id = request.GET.get('customer_id', None)

    customer = User.objects.get(pk=customer_id)
    
    data = {
        'first_name' : customer.first_name,
        'last_name' : customer.last_name,
        'email' : customer.email,
        'contact_no' : customer.profile.contact_no,
        'address' : customer.profile.address,
    }

    return JsonResponse(data)

