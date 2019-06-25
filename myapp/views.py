from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

# Create your views here.
def joinTrip(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    user = User.objects.get(id = request.session['user_id'])
    user.joining.add(trip)
    return redirect("/dashboard")

def viewTrip (request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    all_users = trip.join_trip.all()
    context = {
        'trip': trip,
        'all_users': all_users
    }
    return render(request, "viewTrip.html", context)

def logout(request):
    request.session.clear()
    return redirect("/")

def newTrip(request):
    return render(request, "newTrip.html")

def addTrip(request):
    errors = Trip.objects.tripValidator(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect("/newTrip")
    else:
        trip = Trip.objects.create(destination = request.POST['destination'], plan = request.POST['plan'], start_date=request.POST['start_date'], end_date=request.POST['end_date'], added_by_id = request.session['user_id'])
        user = User.objects.get(id=request.session['user_id'])
        user.joining.add(trip)
        return redirect("/dashboard")


def index(request):
    return render(request, "index.html")

def register(request):
    errors = User.objects.regValidator(request.POST)
    print(errors)
    if errors:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect("/")
    else:
        hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = User.objects.create(name = request.POST['name'], username = request.POST['username'], password =
        hash.decode())
        request.session['user_id']= user.id
        return redirect("/dashboard")

def login(request):
    result = User.objects.loginValidator(request.POST)
    print(result)
    if result[0]:
        for key, value in result[0].items():
            messages.error(request, value, extra_tags=key)
        return redirect('/')
    else:
        request.session["user_id"] = result[1].id
        return redirect("/dashboard")


def dashboard(request):
    if not 'user_id' in request.session:
        messages.add_message(request, messages.INFO, "You need to log in or register first.", extra_tags = 'login')
        return redirect('/')
    # all_trips = Trip.objects.exclude(users = request.session['user_id'])
    # context = {
    #     # 'trips': User.objects.get(id=request.session['user_id']).trips.all(),
    #     'all_trips': Trip.objects.exclude(users = request.session['user_id'])
    #     }

    user = User.objects.get(id=request.session['user_id'])
    all_trips = Trip.objects.all()
    my_trips = user.joining.all()
    context = {
                "user": user,
                "all_trips": all_trips,
                "my_trips": my_trips,
                "other_trips": all_trips.difference(my_trips)
              }
    return render(request, "dashboard.html", context)
