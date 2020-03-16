from django.test import TestCase, Client
from django.urls import reverse

from django.contrib.auth.models import User
from home.models import Profile, RoomManager, Rooms, TimeSlot, PreBookingAllowance, Booking

from datetime import datetime, date, timedelta

# Index View Testing Starts

class IndexViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create two User
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')
        
        test_user1.save()
        test_user2.save()

        # Complete profile of first user
        test_user1.first_name = 'test'
        test_user1.last_name = 'user'
        test_user1.email = 'test_user@email.com'
        test_user1.save()
        test_user1_profile = Profile.objects.create(
            user = test_user1,
            gender = 'M',
            contact_no = '9999985641',
            address = 'Jabalpur'
        )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
           
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_redirect_if_logged_in_and_profile_complete(self):
        #  Login the User 1 (having complete profile)
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('home'))

        # Check it redirects correctly to dashboard
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard'))

    def test_redirect_if_logged_in_and_profile_not_complete(self):
        #  Login the User 2 (having incomplete profile)
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('home'))

        # Check it redirects correctly to setprofile
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('setprofile'))

    def test_correct_template_is_loaded(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'home/index.html')

    def test_view_login_with_correct_data(self):
        response = self.client.post(reverse('home'), {
            'username' : 'testuser1',
            'password' : '1X<ISRUkw+tuK',
            'submit' : 'login'
        })

        # Check it redirects correctly to dashboard
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard'))

    def test_view_login_with_incorrect_username(self):
        response = self.client.post(reverse('home'), {
            'username' : 'incorrectname',
            'password' : '1X<ISRUkw+tuK',
            'submit' : 'login'
        })

        # Check it renders correct template with correct error message
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')
        self.assertEqual(response.context['login_error'], 'Invalid Username or Password')

    def test_view_login_with_incorrect_password(self):
        response = self.client.post(reverse('home'), {
            'username' : 'testuser1',
            'password' : 'incorrect',
            'submit' : 'login'
        })

        # Check it renders correct template with correct error message
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')
        self.assertEqual(response.context['login_error'], 'Invalid Username or Password')

    def test_view_signup_with_valid_data(self):
        response = self.client.post(reverse('home'), {
            'username' : 'testuser3',
            'password1' : 'passww',
            'password2' : 'passww',
            'submit' : 'signup'
        })

        # Check it redirects correctly to setprofile
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.all().count(), 3)
        self.assertRedirects(response, reverse('setprofile'))

    def test_view_signup_with_existing_user(self):
        response = self.client.post(reverse('home'), {
            'username' : 'testuser1',
            'password1' : 'passww',
            'password2' : 'passww',
            'submit' : 'signup'
        })

        # Check it renders correct template with correct error message
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.all().count(), 2)
        self.assertTemplateUsed(response, 'home/index.html')
        self.assertEqual(response.context['signup_error'], 'Account with entered username already exists')

    def test_view_signup_with_mismatching_password(self):
        response = self.client.post(reverse('home'), {
            'username' : 'testuser3',
            'password1' : 'passww',
            'password2' : 'passwwee',
            'submit' : 'signup'
        })

        # Check it renders correct template with correct error message
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.all().count(), 2)
        self.assertTemplateUsed(response, 'home/index.html')
        self.assertEqual(response.context['signup_error'], "Passwords don't match")


# Dashboard View Testing Starts

class DashboardViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create three User
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')
        test_user3 = User.objects.create_user(username='testuser3', password='HGfdgvF677FYV')

        test_user1.save()
        test_user2.save()
        test_user3.save()

        # test_user1 will have incomplete profile

        # Complete Profile of test_user2 with Customer Post
        test_user2.first_name = 'test2'
        test_user2.last_name = 'user2'
        test_user2.email = 'testuser2@email.com'
        test_user2.save()
        test_user2_profile = Profile.objects.create(
            user = test_user2,
            gender = 'M',
            contact_no = '9954556641',
            address = 'Jabalpur',
        )

        # Complete Profile of test_user3 with Room Manager Post
        test_user3.first_name = 'test3'
        test_user3.last_name = 'user3'
        test_user3.email = 'testuser3@email.com'
        test_user3.save()
        test_user3_profile = Profile.objects.create(
            user = test_user3,
            gender = 'M',
            contact_no = '6958746641',
            address = 'Jabalpur',
            room_manager = True,
        )

    def setUp(self):
        # Create a Rooms instance
        self.rooms_obj1 = Rooms.objects.create(rooms=7, start_date=date.today())
        
        # Create two Time Slots instances
        start_time1 = datetime.strptime("13:00", '%H:%M').time()
        end_time1 = datetime.strptime("15:00", '%H:%M').time()
        self.time_slot1 = TimeSlot.objects.create(start_time=start_time1, end_time=end_time1, start_date=date.today())

        start_time2 = datetime.strptime("17:00", '%H:%M').time()
        end_time2 = datetime.strptime("19:00", '%H:%M').time()
        self.time_slot2 = TimeSlot.objects.create(start_time=start_time2, end_time=end_time2, start_date=date.today())

        # Create Pre-Booking Allowance Instance
        self.allowance1 = PreBookingAllowance.objects.create(days=5)

    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 200)
           
    def test_view_url_accessible_by_name(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('dashboard'))

        # Check it redirects correctly to home
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    def test_redirect_if_logged_in_and_profile_not_complete(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('dashboard'))

        # Check it redirects correctly to setprofile
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('setprofile'))

    def test_correct_template_is_loaded(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('dashboard'))
        self.assertTemplateUsed(response, 'home/dashboard.html')

    def test_correct_data_loaded_in_context_with_no_bookings(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')

        # Delete Pre-Booking Allowance already created
        # PreBookingAllowance.objects.get(id=1).delete()

        response = self.client.get(reverse('dashboard'))

        self.assertEqual(response.context['user_bookings'].count(), 0)
        self.assertEqual(response.context['all_bookings'].count(), 0)
        self.assertEqual(response.context['allowance'].days, 5)
        self.assertEqual(response.context['rooms_context1'], '7')
        self.assertEqual(response.context['rooms_context2'], '')
        self.assertEqual(len(response.context['time_slots_list']), 2)

    def test_correct_data_loaded_in_context_with_bookings(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')

        # Create a Booking
        customer = User.objects.get(username='testuser2')
        booking_date = date.today() + timedelta(days=1)
        room = 2
        time_slot = TimeSlot.objects.get(id=1)
        room_manager = RoomManager.objects.get(id=1)

        booking1 = Booking.objects.create(customer=customer, date=booking_date, room=room, time_slot=time_slot, room_manager=room_manager)

        response = self.client.get(reverse('dashboard'))

        self.assertEqual(response.context['user_bookings'].count(), 1)
        self.assertEqual(response.context['user_bookings'].first().customer.username, 'testuser2')
        self.assertEqual(response.context['all_bookings'].count(), 1)
        self.assertEqual(response.context['allowance'].days, 5)
        self.assertEqual(response.context['rooms_context1'], '7')
        self.assertEqual(response.context['rooms_context2'], '')
        self.assertEqual(len(response.context['time_slots_list']), 2)

    def test_view_book_room_feature(self):
        # POST data will always be valid as it is validated by AJAX beforehand
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')

        tomorrow_date = date.today() + timedelta(days=1)
        tomorrow_date_str = tomorrow_date.strftime('%Y-%m-%d')

        # Send POST data
        response = self.client.post(reverse('dashboard'), {
            'booked-on' : tomorrow_date_str,
            'booking-room' : 1,
            'booking-time-slot' : 1,
            'submit' : 'book-room',
        })

        # Check Booking instance created correctly
        booking = Booking.objects.get(id=1)
        self.assertEqual(booking.customer.username, 'testuser2')
        self.assertEqual(booking.room, 1)
        self.assertEqual(booking.time_slot.id, 1)
        self.assertEqual(booking.date, tomorrow_date)

        # Check it redirects correctly to dashboard
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard'))

    def test_view_allowance_update_feature_with_valid_data(self):
        # Login Room Manager
        login = self.client.login(username='testuser3', password='HGfdgvF677FYV')

        # Send POST data
        response = self.client.post(reverse('dashboard'), {
            'allowance' : 7,
            'submit' : 'allowance',
        })

        # Check Booking instance created correctly
        allowance = PreBookingAllowance.objects.get(id=2)
        self.assertEqual(allowance.days, 7)

        # Check it redirects correctly to dashboard
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard'))

    def test_view_allowance_update_feature_with_invalid_data(self):
        # Login Room Manager
        login = self.client.login(username='testuser3', password='HGfdgvF677FYV')

        # Send POST data
        response = self.client.post(reverse('dashboard'), {
            'allowance' : -2,
            'submit' : 'allowance',
        })

        # Check it renders correct template with correct error message
        self.assertEqual(response.status_code, 200)
        self.assertEqual(PreBookingAllowance.objects.all().count(), 1)
        self.assertTemplateUsed(response, 'home/dashboard.html')
        self.assertEqual(response.context['allowance_error'], 'Please enter a valid Pre-Booking Allowance!')

    def test_view_rooms_update_feature_with_invalid_data(self):
        # Login Room Manager
        login = self.client.login(username='testuser3', password='HGfdgvF677FYV')

        # Send POST data
        response = self.client.post(reverse('dashboard'), {
            'rooms' : -2,
            'submit' : 'rooms',
        })

        # Check it renders correct template with correct error message
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Rooms.objects.all().count(), 1)
        self.assertTemplateUsed(response, 'home/dashboard.html')
        self.assertEqual(response.context['rooms_error'], 'Please enter valid Number of Rooms!')

    def test_view_rooms_update_feature_with_valid_data_and_no_previous_bookings(self):
        # Login Room Manager
        login = self.client.login(username='testuser3', password='HGfdgvF677FYV')

        # Send POST data
        response = self.client.post(reverse('dashboard'), {
            'rooms' : 10,
            'submit' : 'rooms',
        })

        today_date = date.today()
        tomorrow_date = today_date + timedelta(days=1)

        # Check Booking instance created correctly
        old_rooms = Rooms.objects.get(id=1)
        self.assertEqual(old_rooms.end_date, today_date)

        new_rooms = Rooms.objects.get(id=2)
        self.assertEqual(new_rooms.rooms, 10)
        self.assertEqual(new_rooms.start_date, tomorrow_date)

        # Check it redirects correctly to dashboard
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard'))

    def test_view_rooms_update_feature_with_valid_data_and_previous_bookings(self):
        # Login Room Manager
        login = self.client.login(username='testuser3', password='HGfdgvF677FYV')

        # Create a Booking Instance
        customer = User.objects.get(username='testuser2')
        booking_date = date.today() + timedelta(days=1)
        room = 2
        time_slot = TimeSlot.objects.get(id=1)
        room_manager = RoomManager.objects.get(id=1)

        booking1 = Booking.objects.create(customer=customer, date=booking_date, room=room, time_slot=time_slot, room_manager=room_manager)

        # Send POST data
        response = self.client.post(reverse('dashboard'), {
            'rooms' : 10,
            'submit' : 'rooms',
        })

        last_booking_date = booking_date
        next_to_last_booking_date = last_booking_date + timedelta(days=1)

        # Check Booking instance created correctly
        old_rooms = Rooms.objects.get(id=1)
        self.assertEqual(old_rooms.end_date, last_booking_date)

        new_rooms = Rooms.objects.get(id=2)
        self.assertEqual(new_rooms.rooms, 10)
        self.assertEqual(new_rooms.start_date, next_to_last_booking_date)

        # Check it redirects correctly to dashboard
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard'))

    def test_view_time_slots_update_feature_with_invalid_data(self):
        # Login Room Manager
        login = self.client.login(username='testuser3', password='HGfdgvF677FYV')

        # Send POST data
        response = self.client.post(reverse('dashboard'), {
            'start_time' : '17:00',
            'end_time' : '5:00',
            'submit' : 'time_slot',
        })

        # Check it renders correct template with correct error message
        self.assertEqual(response.status_code, 200)
        self.assertEqual(TimeSlot.objects.all().count(), 2)
        self.assertTemplateUsed(response, 'home/dashboard.html')
        self.assertEqual(response.context['time_slot_error'], 'Please select a valid time slot!')

    def test_view_time_slots_update_feature_with_overlapping_time_slots(self):
        # Login Room Manager
        login = self.client.login(username='testuser3', password='HGfdgvF677FYV')

        # Send POST data
        response = self.client.post(reverse('dashboard'), {
            'start_time' : '14:00',
            'end_time' : '16:00',
            'submit' : 'time_slot',
        })

        # Check it renders correct template with correct context
        self.assertEqual(response.status_code, 200)
        self.assertEqual(TimeSlot.objects.all().count(), 2)
        self.assertTemplateUsed(response, 'home/dashboard.html')
        self.assertEqual(len(response.context['del_time_slots_list']), 1)
        self.assertEqual(response.context['entered_start_time'], '14:00')
        self.assertEqual(response.context['entered_end_time'], '16:00')

    def test_view_time_slots_update_feature_with_overlapping_deleted_time_slots(self):
        # Login Room Manager
        login = self.client.login(username='testuser3', password='HGfdgvF677FYV')

        today_date = date.today()
        tomorrow_date = today_date + timedelta(days=1)

        # Close (Delete) an existing instance of time slot
        self.time_slot1.end_date = today_date
        self.time_slot1.save()

        # Send POST data
        response = self.client.post(reverse('dashboard'), {
            'start_time' : '14:00',
            'end_time' : '16:00',
            'submit' : 'time_slot',
        })

        # Check Time Slot instance created correctly
        time_slot = TimeSlot.objects.get(id=3)
        self.assertEqual(str(time_slot.start_time), '14:00:00')
        self.assertEqual(str(time_slot.end_time), '16:00:00')
        self.assertEqual(time_slot.start_date, tomorrow_date)

        # Check it redirects correctly to dashboard
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard'))

    def test_view_time_slots_update_feature_with_non_overlapping_time_slots(self):
        # Login Room Manager
        login = self.client.login(username='testuser3', password='HGfdgvF677FYV')

        today_date = date.today()

        # Send POST data
        response = self.client.post(reverse('dashboard'), {
            'start_time' : '01:00',
            'end_time' : '05:00',
            'submit' : 'time_slot',
        })

        # Check Time Slot instance created correctly
        time_slot = TimeSlot.objects.get(id=3)
        self.assertEqual(str(time_slot.start_time), '01:00:00')
        self.assertEqual(str(time_slot.end_time), '05:00:00')
        self.assertEqual(time_slot.start_date, today_date)

        # Check it redirects correctly to dashboard
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard'))

    def test_view_delete_overlapping_time_slot_and_add_new(self):
        # Login Room Manager
        login = self.client.login(username='testuser3', password='HGfdgvF677FYV')

        today_date = date.today()
        tomorrow_date = today_date + timedelta(days=1)

        # Send POST data
        response = self.client.post(reverse('dashboard'), {
            'start_time' : '14:00',
            'end_time' : '16:00',
            'submit' : 'del_ts',
        })

        # Check older Time Slot instance deleted correctly
        time_slot = TimeSlot.objects.get(id=1)
        self.assertEqual(time_slot.end_date, today_date)

        # Check new Time Slot instance created correctly
        time_slot = TimeSlot.objects.get(id=3)
        self.assertEqual(str(time_slot.start_time), '14:00:00')
        self.assertEqual(str(time_slot.end_time), '16:00:00')
        self.assertEqual(time_slot.start_date, tomorrow_date)

        # Check it redirects correctly to dashboard
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard'))

    def test_view_update_profile(self):
        login = self.client.login(username='testuser3', password='HGfdgvF677FYV')

        # Send POST data
        response = self.client.post(reverse('dashboard'), {
            'first_name' : 'test3',
            'last_name' : 'useruser',
            'email' : 'testuser33@gmail.com',
            'gender' : 'M',
            'contact_no' : '9574236542',
            'address' : 'Jabalpur',
            'submit' : 'update-profile',
        })

        # Check Profile updated successfully
        test_user3 = User.objects.get(id=3)
        test_user3_profile = Profile.objects.get(user=test_user3)
        self.assertEqual(test_user3.first_name, 'test3')
        self.assertEqual(test_user3.last_name, 'useruser')
        self.assertEqual(test_user3.email, 'testuser33@gmail.com')
        self.assertEqual(test_user3_profile.gender, 'M')
        self.assertEqual(test_user3_profile.contact_no, '9574236542')
        self.assertEqual(test_user3_profile.address, 'Jabalpur')

        # Check it redirects correctly to dashboard
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard'))


# SetProfile View Testing Starts

class SetProfileViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create two User
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')
        
        test_user1.save()
        test_user2.save()

        # Complete profile of User1
        test_user1.first_name = 'test'
        test_user1.last_name = 'user'
        test_user1.email = 'test_user@email.com'
        test_user1.save()
        test_user1_profile = Profile.objects.create(
            user = test_user1,
            gender = 'M',
            contact_no = '9999985641',
            address = 'Jabalpur'
        )

    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get('/setprofile/')
        self.assertEqual(response.status_code, 200)
           
    def test_view_url_accessible_by_name(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('setprofile'))
        self.assertEqual(response.status_code, 200)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('setprofile'))

        # Check it redirects correctly to dashboard
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    def test_redirect_if_logged_in_and_profile_complete(self):
        #  Login the User 1 (having complete profile)
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('setprofile'))

        # Check it redirects correctly to dashboard
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard'))

    def test_correct_template_is_loaded(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('setprofile'))
        self.assertTemplateUsed(response, 'home/setprofile.html')

    def test_view_when_data_provided_through_POST(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')

        # Send POST data
        response = self.client.post(reverse('setprofile'), {
            'first_name' : 'test2',
            'last_name' : 'user2',
            'email' : 'testuser2@gmail.com',
            'gender' : 'M',
            'contact_no' : '9574236542',
            'address' : 'Jabalpur',
            'sumbit' : 'submit',
        })

        # Check Profile updated successfully
        test_user2 = User.objects.get(id=2)
        test_user2_profile = Profile.objects.get(user=test_user2)
        self.assertEqual(Profile.objects.all().count(), 2)
        self.assertEqual(test_user2.first_name, 'test2')
        self.assertEqual(test_user2.last_name, 'user2')
        self.assertEqual(test_user2.email, 'testuser2@gmail.com')
        self.assertEqual(test_user2_profile.gender, 'M')
        self.assertEqual(test_user2_profile.contact_no, '9574236542')
        self.assertEqual(test_user2_profile.address, 'Jabalpur')

        # Check it redirects correctly to dashboard
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard'))



# Delete Time Slot View Testing Starts

class DeleteTimeSlotViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create two User
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')
        
        test_user1.save()
        test_user2.save()

        # Complete profile of User1 as Customer
        test_user1.first_name = 'test1'
        test_user1.last_name = 'user1'
        test_user1.email = 'test_user1@email.com'
        test_user1.save()
        test_user1_profile = Profile.objects.create(
            user = test_user1,
            gender = 'M',
            contact_no = '9999985641',
            address = 'Jabalpur',
        )

        # Complete profile of User1 as Room Manager
        test_user2.first_name = 'test2'
        test_user2.last_name = 'user2'
        test_user2.email = 'test_user2@email.com'
        test_user2.save()
        test_user2_profile = Profile.objects.create(
            user = test_user2,
            gender = 'M',
            contact_no = '9999985641',
            address = 'Jabalpur',
            room_manager = True,
        )

    def setUp(self):
        # Create a Rooms instance
        self.rooms_obj1 = Rooms.objects.create(rooms=7, start_date=date.today())
        
        # Create two Time Slots instances
        start_time1 = datetime.strptime("13:00", '%H:%M').time()
        end_time1 = datetime.strptime("15:00", '%H:%M').time()
        self.time_slot1 = TimeSlot.objects.create(start_time=start_time1, end_time=end_time1, start_date=date.today())

        start_time2 = datetime.strptime("17:00", '%H:%M').time()
        end_time2 = datetime.strptime("19:00", '%H:%M').time()
        self.time_slot2 = TimeSlot.objects.create(start_time=start_time2, end_time=end_time2, start_date=date.today())

        # Create Pre-Booking Allowance Instance
        self.allowance1 = PreBookingAllowance.objects.create(days=5)

    def test_view_redirects_correctly(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('delete_ts', args=[1]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard'))

    def test_view_deletes_time_slot_correctly_without_previous_booking(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('delete_ts', args=[1]))


        # Check Time Slot closed (deleted) successfully
        time_slot = TimeSlot.objects.get(id=1)
        self.assertEqual(time_slot.end_date, date.today())

        # Check it redirects correctly to dashboard
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard'))

    def test_view_deletes_time_slot_correctly_with_previous_booking(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')

        # Create a Booking Instance
        customer = User.objects.get(username='testuser1')
        booking_date = date.today() + timedelta(days=1)
        room = 2
        time_slot = TimeSlot.objects.get(id=1)
        room_manager = RoomManager.objects.get(id=1)

        booking1 = Booking.objects.create(customer=customer, date=booking_date, room=room, time_slot=time_slot, room_manager=room_manager)

        last_booking_date = booking_date

        response = self.client.get(reverse('delete_ts', args=[1]))

        # Check Time Slot closed (deleted) successfully
        time_slot = TimeSlot.objects.get(id=1)
        self.assertEqual(time_slot.end_date, last_booking_date)

        # Check it redirects correctly to dashboard
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard'))


# Delete Booking View Testing Starts

class DeleteBookingViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create two User
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')
        
        test_user1.save()
        test_user2.save()

        # Complete profile of User1 as Customer
        test_user1.first_name = 'test1'
        test_user1.last_name = 'user1'
        test_user1.email = 'test_user1@email.com'
        test_user1.save()
        test_user1_profile = Profile.objects.create(
            user = test_user1,
            gender = 'M',
            contact_no = '9999985641',
            address = 'Jabalpur',
        )

        # Complete profile of User1 as Room Manager
        test_user2.first_name = 'test2'
        test_user2.last_name = 'user2'
        test_user2.email = 'test_user2@email.com'
        test_user2.save()
        test_user2_profile = Profile.objects.create(
            user = test_user2,
            gender = 'M',
            contact_no = '9999985641',
            address = 'Jabalpur',
            room_manager = True,
        )

    def setUp(self):
        # Create a Rooms instance
        self.rooms_obj1 = Rooms.objects.create(rooms=7, start_date=date.today())
        
        # Create two Time Slots instances
        start_time1 = datetime.strptime("13:00", '%H:%M').time()
        end_time1 = datetime.strptime("15:00", '%H:%M').time()
        self.time_slot1 = TimeSlot.objects.create(start_time=start_time1, end_time=end_time1, start_date=date.today())

        start_time2 = datetime.strptime("17:00", '%H:%M').time()
        end_time2 = datetime.strptime("19:00", '%H:%M').time()
        self.time_slot2 = TimeSlot.objects.create(start_time=start_time2, end_time=end_time2, start_date=date.today())

        # Create Pre-Booking Allowance Instance
        self.allowance1 = PreBookingAllowance.objects.create(days=5)

        # Create Booking Instance
        customer = User.objects.get(username='testuser1')
        booking_date = date.today() + timedelta(days=1)
        room = 2
        time_slot = TimeSlot.objects.get(id=1)
        room_manager = RoomManager.objects.get(id=1)

        booking1 = Booking.objects.create(customer=customer, date=booking_date, room=room, time_slot=time_slot, room_manager=room_manager)

    def test_view_redirects_correctly(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('delete_booking', args=[1]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard'))

    def test_view_deletes_booking_correctly(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('delete_booking', args=[1]))

        # Check Booking cancelled (deleted) successfully
        booking = Booking.objects.get(id=1)
        self.assertTrue(booking.cancelled)

        # Check it redirects correctly to dashboard
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard'))
