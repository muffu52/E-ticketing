from django.shortcuts import render
import logging
logger = logging.getLogger("signal")


# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import IndexForm, BookingForm
from .models import Airport, FlightSchedule, FlightReservation
from datetime import datetime
import random
import string

def home(request):
    print("in home view")
    if request.method == 'POST':
        print("inside post method")
        form = IndexForm(request.POST)
        if form.is_valid():
            print("inside valid")
            departure_airport = form.cleaned_data.get('from_place')
            arrival_airport = form.cleaned_data.get('to_place')
            date = form.cleaned_data.get('date')
            print(departure_airport)
            print(arrival_airport)
            print(date)
            queryset = FlightSchedule.objects.select_related('flight').filter(flight__departure__id = departure_airport, flight__arrival__id = arrival_airport, departureTime = date)
            print(queryset)
            # return redirect('home', {'queryset':queryset})
            return render(request, 'flight_list.html', {'queryset':queryset})
        
    else:
        print("inside get method")
        form = IndexForm()
        airports = Airport.objects.all()
        context = {'airports':airports, 'form':form}
        return render(request, 'index.html', context)


def contact(request):
    return render(request, 'contact.html')

def flight(request):
    message = {
    'message' : "user visits fligh page"
    }
    logger.info(message)
    return render(request, 'flight.html')

def manage_booking(request):
    print(request.user.id)
    queryset = FlightReservation.objects.filter(customer__id = request.user.id)
    return render(request, 'manage_booking.html', {'queryset':queryset})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

# def searchFlight(request):
#     if request.method == 'POST':
#         form = IndexForm(request.POST)
#         if form.is_valid():
#             return HttpResponseRedirect('list/')

#     else:
#         form = IndexForm()
#     return render(request, 'index.html', {'form':form})    
# reservationNumber = models.TextField()
#     flightschedule = models.ForeignKey(FlightSchedule, on_delete=models.CASCADE)
#     creationDate = models.DateField()
#     reservationStatus = models.CharField(max_length=10, choices=RESERVATION_STATUS_CHOICES, default="PENDING")
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
def book(request, pk=None):
    if request.method == 'POST':
        print("inside post method")
        form = BookingForm(request.POST)
        print(form.errors)
        if form.is_valid():
            print("inside valid")
            no_adults = form.cleaned_data.get('no_adults')
            no_children = form.cleaned_data.get('no_children')
            reservationNumber = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
            print(no_adults)
            print(no_children)
            print(reservationNumber)
            print(request.user.id)
            reservation = FlightReservation(reservationNumber = reservationNumber, flightschedule_id = pk, creationDate=datetime.today(), reservationStatus="CONFIRMED", customer_id=request.user.id)
            # return redirect('home', {'queryset':queryset})
            reservation.save()
            return redirect('manage_booking')
    else:
        queryset = FlightSchedule.objects.get(id = pk)
        return render(request, 'booking.html', {'queryset':queryset})