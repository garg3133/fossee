# Room Slot Booking
FOSSEE - Room Slot Booking

### Yaksh Account Details
**Username**: priyansh3133  
**Email**: 2018196@iiitdmj.ac.in

## Table of Content
- [Installation](#installation)
    - [Requirements](#requirements)
    - [How to run it?](#how-to-run-it)
- [Usage](#typo3-setup)
    - [Extension](#extension)
    - [Database](#database)
- [Page setup](#page-setup)
    - [Upload the page tree file](#upload-the-page-tree-file)
    - [Go to the import view](#go-to-the-import-view)
    - [Import the uploaded page tree file](#import-the-uploaded-page-tree-file)
- [License](#license)
- [Links](#links)

## Installation
Follow the below instructions to setup and run the app on your local machine.

### Requirements
Python 3.7  
Git  
Django 2.2.8  
And additional requirements are in **requirements.txt**  


### How to run it?
  * Download and install Python 3.7
  * Download and install Git.
  * Fork the Repository.
  * Clone the repository to your local machine `$ git clone https://github.com/<your-github-username>/fossee.git`
  * Change directory to fossee `$ cd fossee`
  * Install virtualenv `$ pip3 install virtualenv`  
  * Create a virtual environment `$ virtualenv env -p python3.7`  
  * Activate the env: `$ source env/bin/activate`
  * Install the requirements: `$ pip3 install -r requirements.txt`
  * Change directory to roomslotbooking `$ cd roomslotbooking`
  * Make migrations `$ python manage.py makemigrations`
  * To Make migrations for a particular app `$ python manage.py makemigrations <App name>`
  * Migrate the changes to the database `$ python manage.py migrate`
  * Create admin `$ python manage.py createsuperuser`
  * Run the server `$ python manage.py runserver`
 
## Usage

### Create an Account
For using the Room Slot Booking App, you must first have an account on the application. Follow the below instructions to *create a new account*.

- Click on the **Login** button on Homepage to get a Login modal.
- Click on **Sign Up** link at the bottom of the modal.
- Enter your *Username* and *Password*.
- Click on **Sign Up** Button.
- After successful Sign Up, you'll be redirected to **Complete your Profile** Page where you'll be asked to enter your personal details.
- Enter the required details and click on **Continue**.

Congratulations, your account has been created successfully.

after that, you'll be automatically logged in into your account and redirected to your dashboard.

### Login into your Account
For logging in and using the Room Slot Booking App, you must first have an account on the applications.

If you don't have an account, follow [Create an Account](#create-an-account) to create a new account.

If you already have an account, follow the below steps to *Login* into your account.

- Click on the **Login** button on Homepage to get a Login modal.
- Enter your *Username* and *Password*.
- Click on **Sign In** button.

After successful Login, you'll be redirected to your dashboard.

## User: Room Manager
Room Manager is the user who will manage the ongoings of the application in terms of number of rooms to be made available to the customers and the time slots for which the rooms can be booked. Plus, he can also define the number of days for which the bookings can be done in advance.

*There can be only one Room Manager at a time.*

>By default, all users are created as *Customers*.

### Promote a User to Room Manager
Only **Admin** or **Superuser** can promote a *User* to *Room Manager* by following the below steps:

- Go to the [Admin Page](https://localhost:8000/admin) of the application.
- Enter your *Username* and *Password* and click on **Log In** button.
- Under **Home** section, click on **Profiles** link.
- Click on the *Username* of the User you wish to promote.
- Tick the **Room manager** checkbox.
- Click on **Save** button.

**Note:** 
1. While promoting a user to Room Manager, if a Room Manager already exists then he'll be automatically demoted from the Room Manager to a normal Customer. 
2. To ensure that at no point of time the application is without a Room Manager, Room Manager cannot be demoted to a Customer until adn unless a new user is promoted to Room Manager.
3. All the changes in the post of Room Manager are stored in the database along with the start and end date of the tenure of each Room Manager.

### View Rooms, Time Slots and Pre-Booking Allowance
The Room Manager can view
- The number of Rooms he made available for the Customers to book from,
- Time Slots for which the Rooms are available, and
- The number of days for which the Customers can place bookings in advance

under the **Home Tab** on his dashboard.

### Update Number of Rooms
To update number of Rooms to be made available for the Customers to book from, follow the below steps:

- On your *Dashboard*, click on the **Manage Rooms** dropdown pill.
- Under **Manage Rooms** dropdown, click on **No. of Rooms**.
- Enter the U*pdated Number of Rooms* to be made available to the Customers in the text field provided (Refer to the table above for currently available Number of Rooms).
- Click on **Update** button.

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
