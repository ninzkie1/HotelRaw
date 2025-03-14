from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class Room(models.Model):
    ROOM_TYPES = [
        ('SINGLE', 'Single'),
        ('DOUBLE', 'Double'),
        ('SUITE', 'Suite'),
    ]

    room_number = models.IntegerField(unique=True)
    room_type = models.CharField(max_length=10, choices=ROOM_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
         return f"Room {self.room_number} - {self.room_type}"

    class Meta:
        ordering = ['room_number']

class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    guest_name = models.CharField(max_length=100)
    guest_email = models.EmailField()
    check_in = models.DateField()
    check_out = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # e check og ang check in gauna ba na date kaysa sa check out
        if self.check_in and self.check_out and self.check_in >= self.check_out:
            raise ValidationError(_('Check-in date must be before check-out date.'))

        # Dili maka book og not avaialble na room
        if not self.room.is_available:
            raise ValidationError(_('This room is currently unavailable and cannot be booked.'))

        # Para dili na ma book ang date na naay booking
        overlapping_bookings = Booking.objects.filter(
            room=self.room,
            check_in__lt=self.check_out,
            check_out__gt=self.check_in
        ).exclude(pk=self.pk)

        if overlapping_bookings.exists():
            raise ValidationError(_('Room is already booked for these dates.'))

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.guest_name} - {self.room.room_number} ({self.check_in} to {self.check_out})"

    class Meta:
        ordering = ['-check_in']
