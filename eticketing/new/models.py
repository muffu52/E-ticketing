from django.db import models
from django.conf import settings

# Create your models here.

class Seat(models.Model):
    seatNumber = models.TextField()
    seatType = models.TextField()
    seatClass = models.TextField()

    def __str__(self):
        return self.seatNumber

class FlightSeat(models.Model):
    BOOKING_STATUS_CHOICES = [
        ("BOOKED", "BOOKED"),
        ("OPEN", "OPEN")
    ]
    fare = models.IntegerField()
    bookingStatus = models.CharField(max_length=10, choices=BOOKING_STATUS_CHOICES, default="OPEN")
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)

    def __str__(self):
        return self.seat.seatNumber

class Customer(models.Model):
    name = models.TextField()
    email =  models.EmailField()
    mobileNo = models.TextField()
    flightSeat = models.OneToOneField(FlightSeat, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Airport(models.Model):
    name = models.TextField()
    address = models.TextField()
    code = models.TextField()

    def __str__(self):
        return self.name

class Flight(models.Model):
    flightNo = models.TextField()
    flightName = models.CharField(max_length=20)
    duration = models.IntegerField()
    departure = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="flight_d")
    arrival = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="flight_a")

    def __str__(self):
        return self.flightNo

class FlightSchedule(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    departureTime = models.DateField()
    arrivalTime = models.DateField()
    gate = models.TextField()
    fare = models.IntegerField()

    def __str__(self):
        return self.flight.flightNo

class FlightReservation(models.Model):
    RESERVATION_STATUS_CHOICES = [
        ("CONFIRMED", 'CONFIRMED'),
        ("PENDING", 'PENDING')
    ]
    reservationNumber = models.TextField()
    flightschedule = models.ForeignKey(FlightSchedule, on_delete=models.CASCADE)
    creationDate = models.DateField()
    reservationStatus = models.CharField(max_length=10, choices=RESERVATION_STATUS_CHOICES, default="PENDING")
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.flightschedule.flight.flightNo