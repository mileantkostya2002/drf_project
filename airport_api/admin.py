
from django.contrib import admin
from .models import (
    Country,
    City,
    Crew,
    AirplaneType,
    Airplane,
    Airport,
    Route,
    Flight,
)

admin.site.register(Country)
admin.site.register(City)
admin.site.register(Crew)
admin.site.register(AirplaneType)
admin.site.register(Airplane)
admin.site.register(Airport)
admin.site.register(Route)
admin.site.register(Flight)