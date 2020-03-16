# Room Slot Booking
![FOSSEE logo](https://fossee.in/sites/all/themes/software_responsive_theme/img/logo.png)  
Room Slot Booking Django Application for Python Screening Test Under FOSSEE 2020  

### Yaksh Account Details
**Username**: priyansh3133  
**Email**: 2018196@iiitdmj.ac.in

## Table of Content
- [Installation](#installation)
    - [Requirements](#requirements)
    - [How to run it?](#how-to-run-it)
    - [Running Tests](#running-tests)
- [Usage](#usage)
    - [Create an Account](#create-an-account)
    - [Login into your Account](#login-into-your-account)
    - [Promote a User to Room Manager](#promote-a-user-to-room-manager)
    - [User: Customer](#user-customer)
        - [Book Room](#book-room)
        - [View Bookings](#view-bookings)
            - [Delete a Booking](#delete-a-booking)
        - [Update Profile](#update-profile)
    - [User: Room Manager](#user-room-manager)
        - [View Rooms, Time Slots and Pre-Booking Allowance](#view-rooms-time-slots-and-pre-booking-allowance)
        - [Update Number of Rooms](#update-number-of-rooms)
        - [Update Time Slots](#update-time-slots)
            - [Add a new Time Slot](#add-a-new-time-slot)
            - [Delete an existing Time Slot](#delete-an-existing-time-slot)
            - [Update an existing Time Slot](#update-an-existing-time-slot)
        - [Update Pre-Booking Allowance](#update-pre-booking-allowance)
        - [View the Summary of all the Previous Bookings](#view-the-summary-of-all-the-previous-bookings)
        - [Update Profile](#update-profile-1)

## Installation
Follow the below instructions to setup and run the app on your local machine.

### Requirements
Python 3.7  
Git  
Django 2.2.8  
And additional requirements are in **requirements.txt**  


### How to run it?
- Download and install Python 3.7
- Download and install Git.
- Fork the Repository.
- Clone the repository to your local machine `$ git clone https://github.com/<your-github-username>/fossee.git`
- Change directory to fossee `$ cd fossee`
- Install virtualenv `$ pip3 install virtualenv`  
- Create a virtual environment `$ virtualenv env -p python3.7`  
- Activate the env: `$ source env/bin/activate`
- Install the requirements: `$ pip3 install -r requirements.txt`
- Change directory to roomslotbooking `$ cd roomslotbooking`
- Make migrations `$ python manage.py makemigrations`
- To Make migrations for a particular app `$ python manage.py makemigrations <App name>`
- Migrate the changes to the database `$ python manage.py migrate`
- Create admin `$ python manage.py createsuperuser`
- Run the server `$ python manage.py runserver`

### Running Tests
- Open Project in **fossee** directory.
- Activate the env: `$ source env/bin/activate`
- Change directory to roomslotbooking `$ cd roomslotbooking`
- Run the tests: `$ ./manage.py test home`
 
## Usage

![2020-03-16](https://user-images.githubusercontent.com/39924567/76780868-bfb08b00-67d3-11ea-9976-944a4f916d03.png)

### Create an Account
For using the Room Slot Booking App, you must first have an account on the application. Follow the below instructions to *create a new account*.

- Click on the **Login** button on Homepage to get a Login modal.
- Click on **Sign Up** link at the bottom of the modal.
- Enter your *Username* and *Password*.
- Click on **Sign Up** Button.
- After successful Sign Up, you'll be redirected to **Complete your Profile** Page where you'll be asked to enter your personal details.
- Enter the required details and click on **Continue**.

![2020-03-16 (3)](https://user-images.githubusercontent.com/39924567/76780944-eb337580-67d3-11ea-9097-944ee0629cdd.png)
![2020-03-16 (5)](https://user-images.githubusercontent.com/39924567/76781185-554c1a80-67d4-11ea-8ecc-37b8acde4c81.png)

Congratulations, your account has been created successfully. You'll be automatically logged into your account and redirected to your dashboard.

>By default, all new Users are designated as *Customers*.

### Login into your Account
For logging in and using the Room Slot Booking App, you must first have an account on the applications. If you don't have an account, follow [Create an Account](#create-an-account) to create a new account. Otherwise, follow the below steps to *Login* into your account.

- Click on the **Login** button on Homepage to get a Login modal.
- Enter your *Username* and *Password*.
- Click on **Sign In** button.

![2020-03-16 (4)](https://user-images.githubusercontent.com/39924567/76781036-14540600-67d4-11ea-9645-acd76afe9bb2.png)

After successful Login, you'll be redirected to your dashboard.

### Promote a User to Room Manager
Only Users with **Admin** or **Superuser** privileges can promote a *User* to *Room Manager* by following the below steps:

- Go to the [Admin Page](https://localhost:8000/admin) of the application.
- Enter your *Username* and *Password* and click on **Log In** button.
- Under **Home** section, click on **Profiles** link.
- Click on the *Username* of the User you wish to promote.
- Tick the **Room manager** checkbox.
- Click on **Save** button.

![2020-03-16 (6)](https://user-images.githubusercontent.com/39924567/76781352-9a704c80-67d4-11ea-89ab-94fcb1258466.png)

**Note:** 
1. While promoting a user to Room Manager, if a Room Manager already exists then he'll be automatically demoted from the Room Manager to a normal Customer. 
2. To ensure that at no point of time the application is without a Room Manager, Room Manager cannot be demoted to a Customer until adn unless a new user is promoted to Room Manager.
3. All the changes in the post of Room Manager are stored in the database along with the start and end date of the tenure of each Room Manager.

## User: Customer
Customer is the user who will use the Room Slot Booking application for booking Rooms.

![2020-03-16 (7)](https://user-images.githubusercontent.com/39924567/76781477-c7bcfa80-67d4-11ea-8dc5-40a902b9a825.png)

### Book Room
To book a Room using the Room Slot Booking application, follow the steps below:

- Click on the **Book Room** pill on the *Dashboard*.
- Select the Date for which the booking is to be made.
- After selecting the Date, if you encounter an error, change the Booking Date accordingly.
- If no error is encountered, the Rooms available on the selected date will get updated in the *Available Rooms* field through AJAX.
- Select the *Room* from the list you wish to book.
- If no *Time Slot* is free for the selected Room on the selected Date, you'll encounter an error. Change the Room or the Date accordingly.
- If you don't encounter any error, the available Time Slots will get updated in the *Available Time Slots* field through AJAX.
- Select the *Time Slot* you wish to book the selected Room for.
- Click on the **Book** button.

![2020-03-16 (8)](https://user-images.githubusercontent.com/39924567/76781697-22eeed00-67d5-11ea-893c-cb48e6aea74d.png)
![2020-03-16 (9)](https://user-images.githubusercontent.com/39924567/76781699-25e9dd80-67d5-11ea-9f0d-e6c702fdacb0.png)
![2020-03-16 (10)](https://user-images.githubusercontent.com/39924567/76781702-26827400-67d5-11ea-8bfe-e398969d5c92.png)

### View Bookings
To view all your Previous Bookings, click on the **My Previous Bookings** pill on the *Dashboard*.

The bookings are arranged in the order the Bookings were made (latest Booking first).
![2020-03-16 (11)](https://user-images.githubusercontent.com/39924567/76781803-487bf680-67d5-11ea-97c7-83f3368b803d.png)

Click on the Room Manager's *Username* corresponding to a Booking to know the details of the Room Manager at the time of Booking.
![2020-03-16 (12)](https://user-images.githubusercontent.com/39924567/76781813-4ade5080-67d5-11ea-9722-509ac40e2548.png)

#### Delete a Booking
To cancel (delete) a Booking, click on the **Cancel** link corresponding to the Booking.

![2020-03-16 (11)](https://user-images.githubusercontent.com/39924567/76781900-6cd7d300-67d5-11ea-91df-9a91b1aef5cf.png)
![2020-03-16 (13)](https://user-images.githubusercontent.com/39924567/76782184-e374d080-67d5-11ea-8bf2-774fec0c663a.png)

### Update Profile
To update your profile, follow the below steps:

- Click on **Update Profile** pill on the *Dashboard*.
- Change the values to be updated in the respective fields.
- Click on the **Update** button.

![2020-03-16 (14)](https://user-images.githubusercontent.com/39924567/76782276-0f905180-67d6-11ea-8a9a-294bdb348b14.png)

## User: Room Manager
Room Manager is the user who will manage the ongoings of the application in terms of number of rooms to be made available to the customers and the time slots for which the rooms can be booked. Plus, he can also define the number of days for which the bookings can be done in advance.

![2020-03-16 (16)](https://user-images.githubusercontent.com/39924567/76782477-57af7400-67d6-11ea-8a8a-2c7c4b2599f9.png)

*There can be only one Room Manager at a time.*

### View Rooms, Time Slots and Pre-Booking Allowance
The Room Manager can view
- The number of Rooms he made available for the Customers to book from,
- Time Slots for which the Rooms are available, and
- The number of days for which the Customers can place bookings in advance.

under the **Home Tab** on his dashboard.

![2020-03-16 (15)](https://user-images.githubusercontent.com/39924567/76782333-2767d580-67d6-11ea-89d5-5f8dce9eb563.png)

### Update Number of Rooms
To update number of Rooms to be made available for the Customers to book from, follow the below steps:

- On your *Dashboard*, click on the **Manage Rooms** dropdown pill.
- Under **Manage Rooms** dropdown, click on **No. of Rooms**.
- Enter the *Updated Number of Rooms* to be made available to the Customers in the text field provided (Refer to the table above for currently available Number of Rooms).
- Click on **Update** button.

![2020-03-16 (17)](https://user-images.githubusercontent.com/39924567/76782560-76156f80-67d6-11ea-8e5e-6e8463067a74.png)

**Note:**
1. If *Number of Rooms* are updated for the first time, the updated number of rooms will take effect immediately.
2. If *Number of Rooms* are not updated for the first time:
    1. If there is no active booking after the day of update, the updated number of rooms will take effect from the next day.
    2. If there are active bookings after the day of update, the updated number of rooms will take effect from the day next to the day of last booking.

### Update Time Slots
To update the Time Slots for which the Rooms are available to be booked, follow the following steps:

- On your *Dashboard*, click on the **Manage Rooms** dropdown pill.
- Under **Manage Rooms** dropdown, click on **Time Slots**.

From here, you can either *add a new Time Slot* or *delete or update an existing Time Slot*.

![2020-03-16 (19)](https://user-images.githubusercontent.com/39924567/76782681-aceb8580-67d6-11ea-8df5-0e523616b8fe.png)
![2020-03-16 (18)](https://user-images.githubusercontent.com/39924567/76782747-c391dc80-67d6-11ea-8036-282069eb1a83.png)

#### Add a new Time Slot
To add a new Time Slot, continue with the following steps:

- Enter the *Start Time* and *End Time* of the new Time Slot in the respective input fields (Refer to the table above for *Current Time Slots*). You can use the *Time Picker* for entering time by clicking on the icon at the end of the input field.
- Click on the **Add** button.
- If the new Time Slot does not overlap with any existing Time Slot,
    - A new Time Slot will be created with effect from the same day.
- If the new Time Slot does not overlap with any existing Time Slot but with an already deleted Time Slot whose deletion has not come into effect yet (due to reasons discussed [later](#delete-an-existing-time-slot)),
    - A new Time Slot will be created but will come into effect from the day when the deletion of all the overlapping Time Slots take effect successfully.
- If the new Time Slot overlaps with the existing Time Slots,
    - A modal will appear asking for deletion of the existing overlapping Time Slots.
    - If you wish to *delete the overlapping Time Slots*, click the **Delete** button. *The addition of the new Time Slot and deletion of the overlapping Time Slots will take effect from the day next to the day of last booking on any of the overlapping Time Slots*.
    - If you *don't* wish to *delete the overlapping Time Slots*, either [Update the overlapping Time Slots](#update-an-existing-time-slot) and then add new Time Slot or change the new Time Slot itself.

**Note:** The Start Time and End Time of the new Time Slot must belong to the same day.

#### Delete an existing Time Slot
To delete an existing Tme Slot, continue with the following steps:

- Click on the **Delete** link corresponding to the Time Slot you wish to delete.

**Note:** If there are no Pre-Bookings made for the deleted Time Slot, the deletion will take effect from the very next day. Otherwise, the deletion of the Time Slot will take effect from the day next to the day of last Pre-Booking for that Time Slot.

#### Update an existing Time Slot
To update an existing Tme Slot, continue with the following steps:

- [Delete](delete-an-existing-time-slot) the Time Slot to be updated.
- [Add](#add-a-new-time-slot) the updated new Time Slot.

All the updates will take atleast one day to come into effect (the day on which it is updated) in the best case (if there are no Pre-Bookings on the previous Time Slot and the updated new Time Slot does not overlaps with any other existing Time Slot).

### Update Pre-Booking Allowance
Pre-Booking Allowance refers to the number of days for which the Customers can book Rooms in advance.

To update the Pre-Booking Allowance, follow the below steps:

- On your *Dashboard*, click on the **Manage Rooms** dropdown pill.
- Under **Manage Rooms** dropdown, click on **Pre-Booking Allowance**.
- Enter the *Updated Pre-Booking Allowance* in the text field provided (Refer to the table above for current Pre-Booking Allowance).
- Click on **Update** button.

![2020-03-16 (20)](https://user-images.githubusercontent.com/39924567/76782830-e1f7d800-67d6-11ea-9acc-4d30cedee3d4.png)

Unlike the updation in Number of Rooms and Time Slots, the updation in Pre-Booking Allowance will take effect from the very moment it is updated.

### View the Summary of all the Previous Bookings
Click on the **Bookings Summary** pill on the *Dashboard* to view the Summary of all the previous, current and future Bookings.

The bookings are arranged in the order of Date (latest Date first) and then the ascending order of Room Number and Time Slot.

![2020-03-16 (21)](https://user-images.githubusercontent.com/39924567/76782967-123f7680-67d7-11ea-922c-82475609585d.png)

Click on the Customer's *Username* corresponding to a Booking to know the details of the Customer and on the Room Manager's *Username* to know the details of the Room Manager at the time of Booking.

![2020-03-16 (22)](https://user-images.githubusercontent.com/39924567/76782970-14a1d080-67d7-11ea-862c-94a9d71e6a14.png)
![2020-03-16 (23)](https://user-images.githubusercontent.com/39924567/76782978-15d2fd80-67d7-11ea-87db-19bb026b3510.png)

### Update Profile
To update your profile, follow the below steps:

- Click on **Update Profile** pill on the *Dashboard*.
- Change the values to be updated in the respective fields.
- Click on the **Update** button.

![2020-03-16 (14)](https://user-images.githubusercontent.com/39924567/76782276-0f905180-67d6-11ea-8a9a-294bdb348b14.png)
