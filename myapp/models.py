from django.db import models
import re
import bcrypt
from datetime import datetime, time, date
from time import strftime
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your models here.
class UserManager(models.Manager):
    def regValidator(self, form):
        name = form['name']
        username = form['username']
        password = form['password']
        confirm_pw = form['confirm_pw']

        errors ={}

        if not name:
            errors['name'] = "Name can not be blank"
        elif len(name) < 3:
            errors['name'] = "Name must be more than 3 characters."

        if not username:
            errors['reg_username'] = "Username can not be blank."
        elif len(username) < 3:
            errors['reg_username'] = "Username must be more than 3 characters."
        elif User.objects.filter(username=username):
            errors['reg_username'] = "Username already exists. Please log in."

        if not password:
            errors['reg_password'] = "Password can not be blank."
        elif len(password) < 8:
            errors['reg_password'] = "Password must be 8 characters or more."

        if not confirm_pw:
            errors['confirm_pw'] = "Please enter a password."
        elif password != confirm_pw:
            errors['confirm_pw'] = "Passwords do not match."

        return errors

    def loginValidator(self, form):
        username = form['login_username']
        password = form['login_password']
        # user = User.objects.get(username=username)
        errors = {}

        if username and not password:
            errors['login_password'] = "Please fill out your password."
        if not password:
            errors['login_password'] = "Password can not be blank."
        if not username:
            errors['login_username'] = "Username can not be blank."
        elif not User.objects.filter(username=username):
                errors['login_username'] = "Username not found. Please register."
        else:
            if not password:
                errors['login_password'] = "Password required."
            else:
                user = User.objects.get(username=username)
                if not bcrypt.checkpw(password.encode(), user.password.encode()):
                    errors['login_password'] = "Incorrect password. Please try again."

            return errors, user

        return errors, False

class TripManager(models.Manager):
    def tripValidator(self, form):
        d = datetime.now()
        now=d.strftime("%Y-%m-%d")
        destination = form['destination']
        plan = form['plan']
        start_date = form['start_date']
        end_date = form['end_date']

        errors = {}

        if not destination:
            errors['destination'] = "Destination can not be blank."
        if not plan:
            errors['plan'] = "What is your itinerary?"
        if not start_date:
            errors['start_date'] = "Please enter a start date."
        elif start_date < now:
            errors['start_date'] = "Please enter a date after today for your trip."
        if not end_date:
            errors['end_date'] = "Please enter an end date."
        elif end_date < start_date:
            errors['end_date'] = "End date must be later than the start date."

        return errors

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    start_date = models.DateTimeField(default="1999-09-09")
    end_date = models.DateTimeField(default="1999-09-25")
    plan = models.TextField(max_length=1000)
    added_by = models.ForeignKey(User, related_name = 'trips_added', on_delete=models.CASCADE)
    join_trip = models.ManyToManyField(User, related_name = 'joining')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()
