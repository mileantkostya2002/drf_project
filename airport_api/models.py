import pathlib
import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify
from typing import Union



class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)

class City(models.Model):
    name = models.CharField(max_length=100, unique=True)
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name="cities",
    )

    class Meta:
        verbose_name_plural = "Cities"
        unique_together = ("name", "country")

    def __str__(self):
        return f"{self.name}({self.country.name})"

class Airport(models.Model):
    name = models.CharField(max_length=255)
    closest_big_city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name="airports"
    )


    def __str__(self):
        country = self.closest_big_city.country.name
        return f"{self.name} ({self.closest_big_city.name}, {country})"



class Route(models.Model):
    source = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='outbound_routes')
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='inbound_routes')
    distance = models.IntegerField()

    @staticmethod
    def validate_route(source, destination, distance, error_to_raise):
        if distance <= 0:
            raise error_to_raise("Distance must be positive")
        if source == destination:
            raise error_to_raise("Source and destination must be different")

    def clean(self):
        Route.validate_route(
            self.source,
            self.destination,
            self.distance,
            ValidationError
        )

    def save(
            self,
            *args,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None
    ):
        self.full_clean()
        return super(Route, self).save(
            force_insert, force_update, using, update_fields
        )

    def __str__(self):
        source_country = self.source.closest_big_city.country.name
        destination_country = self.destination.closest_big_city.country.name
        return (f"{self.source.closest_big_city.name}"
                f"({source_country})"
                f"-> "
                f"{self.destination.closest_big_city.name}"
                f"({destination_country})")

def upload_image_path(
        instance: Union["AirplaneType", "Airport"],
        filename: str
) -> pathlib.Path:
    filename = (
            f"{slugify(instance.name)}-{uuid.uuid4()}.{filename}"
            + pathlib.Path(filename).suffix
    )
    return (
            pathlib.Path(f"upload/{type(instance).__name__}/")
            / pathlib.Path(filename)
    )

class AirplaneType(models.Model):
    name = models.CharField(max_length=150)
    image = models.ImageField(
        null=True,
        blank=True,
        upload_to=upload_image_path
    )

    class Meta:
        verbose_name = "airplane type"
        verbose_name_plural = "airplane types"

    def __str__(self):
        return self.name


class Airplane(models.Model):
    name = models.CharField(max_length=150, unique=True)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()
    airplane_type = models.ForeignKey(AirplaneType, on_delete=models.CASCADE)

    @property
    def capacity(self) -> int:
        return self.rows * self.seats_in_row

    def __str__(self):
        return self.name

class Flight(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE)
    departure_time = models.DateTimeField(null=False, blank=False)
    arrival_time = models.DateTimeField(null=False, blank=False)

    @staticmethod
    def validate_flight(arrival_time, departure_time, error_to_raise):
        if not (departure_time
                and arrival_time
                and departure_time < arrival_time):
            raise error_to_raise(
                "Departure time must be earlier than arrival time"
            )

    def clean(self):
        Flight.validate_flight(
            self.arrival_time,
            self.departure_time,
            ValidationError
        )

    def save(
            self,
            *args,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None
    ):
        self.full_clean()
        return super(Flight, self).save(
            force_insert, force_update, using, update_fields
        )

    def __str__(self):
        return (f"{self.route.source.closest_big_city.name}"
                f"({self.departure_time}) -> "
                f"{self.route.destination.closest_big_city.name}"
                f"({self.arrival_time})")


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    def __str__(self):
        return str(self.created_at)

    class Meta:
        ordering = ["-created_at"]

class Ticket(models.Model):
    seat = models.IntegerField()
    row = models.IntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='tickets')
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='tickets')

    @staticmethod
    def validate_ticket(row, seat, airplane, error_to_raise):
        for ticket_attr_value, ticket_attr_name, airplane_attr_name in [
            (row, "row", "rows"),
            (seat, "seat", "seats_in_row"),
        ]:
            count_attrs = getattr(airplane, airplane_attr_name)
            if not (1 <= ticket_attr_value <= count_attrs):
                raise error_to_raise(
                    {
                        ticket_attr_name: f"{ticket_attr_name} "
                                          f"number must be in available range: "
                                          f"(1, {airplane_attr_name}): "
                                          f"(1, {count_attrs})"
                    }
                )

    def clean(self):
        Ticket.validate_ticket(
            self.row,
            self.seat,
            self.flight.airplane,
            ValidationError,
        )

    def save(
            self,
            *args,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None,
    ):
        self.full_clean()
        return super(Ticket, self).save(
            force_insert, force_update, using, update_fields
        )

    def __str__(self):
        return (
            f"{str(self.flight)} (row: {self.row}, seat: {self.seat})"
        )

    class Meta:
        unique_together = ("flight", "row", "seat")
        ordering = ["row", "seat"]

class Crew(models.Model):
    first_name = models.CharField(max_length=100, null=False)
    last_name = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.first_name + " " + self.last_name

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

