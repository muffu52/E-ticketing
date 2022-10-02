from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Seat)
admin.site.register(FlightSeat)
admin.site.register(Customer)
admin.site.register(Airport)
admin.site.register(Flight)
admin.site.register(FlightSchedule)
admin.site.register(FlightReservation)