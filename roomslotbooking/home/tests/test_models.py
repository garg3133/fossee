from django.test import TestCase

from django.contrib.auth.models import User
from home.models import Profile, RoomManager, Rooms, TimeSlot, PreBookingAllowance, Booking

from datetime import datetime, date

class TestModels(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create two User
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')
        
        test_user1.save()
        test_user2.save()

        # Complete Profile of test_user1
        test_user1.first_name = 'test1'
        test_user1.last_name = 'user1'
        test_user1.email = 'testuser1@email.com'
        test_user1.save()
        test_user1_profile = Profile.objects.create(
            user = test_user1,
            gender = 'M',
            contact_no = '9954556641',
            address = 'Jabalpur',
        )

        # Complete Profile of test_user2
        test_user2.first_name = 'test2'
        test_user2.last_name = 'user2'
        test_user2.email = 'testuser2@email.com'
        test_user2.save()
        test_user2_profile = Profile.objects.create(
            user = test_user2,
            gender = 'M',
            contact_no = '6958746641',
            address = 'Jabalpur',
        )

    # Test Profile save method
    def test_promotion_to_room_manager_creates_new_RoomManager_instance(self):
        self.assertEqual(RoomManager.objects.all().count(), 0)

        # Promote to Room Manager
        test_user1_profile = Profile.objects.get(id=1)
        test_user1_profile.room_manager = True
        test_user1_profile.save()

        # Check creation of instance
        self.assertEqual(RoomManager.objects.all().count(), 1)

        # Fetch the Room Manager Instance
        room_manager = RoomManager.objects.get(id=1)

        # Check the instance is created correctly
        self.assertEqual(room_manager.manager, test_user1_profile.user)

    def test_promotion_to_room_manager_removes_previous_manager(self):
        self.assertEqual(RoomManager.objects.all().count(), 0)

        # Promote of First Room Manager
        test_user1_profile = Profile.objects.get(id=1)
        test_user1_profile.room_manager = True
        test_user1_profile.save()

        # Check creation of instance
        self.assertEqual(RoomManager.objects.all().count(), 1)

        # Promote of Second Room Manager
        test_user2_profile = Profile.objects.get(id=2)
        test_user2_profile.room_manager = True
        test_user2_profile.save()

        # Check removal of first Room Manager
        self.assertFalse(Profile.objects.get(id=1).room_manager)
        self.assertTrue(len(str(RoomManager.objects.get(id=1).tenure_end)) > 0)

        # Check creattion of new instance
        self.assertEqual(RoomManager.objects.all().count(), 2)
        room_manager = RoomManager.objects.get(id=2)
        self.assertEqual(room_manager.manager, test_user2_profile.user)