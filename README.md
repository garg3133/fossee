# Jagrati
FOSSEE - Room Slot Booking

## Requirements

Python 3.7  
Django 2.2.8  
And additional requirements are in **requirements.txt**  


## How to run it?

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
 

