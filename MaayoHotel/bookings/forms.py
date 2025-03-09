from django import forms
from .models import Room, Booking
from datetime import date

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_number', 'room_type', 'price', 'description', 'is_available']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['room', 'guest_name', 'guest_email', 'check_in', 'check_out']
        widgets = {
            'check_in': forms.DateInput(attrs={'type': 'date'}),
            'check_out': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')
        room = cleaned_data.get('room')

        if check_in and check_out and room:
            # Validate check-in date is not in the past
            if check_in < date.today():
                raise forms.ValidationError("Check-in date cannot be in the past.")

            # Validate check-in is before check-out
            if check_in >= check_out:
                raise forms.ValidationError("Check-in date must be before check-out date.")

            # Check room availability
            overlapping_bookings = Booking.objects.filter(
                room=room,
                check_in__lt=check_out,
                check_out__gt=check_in
            )
            
            # Exclude current booking when editing
            if self.instance.pk:
                overlapping_bookings = overlapping_bookings.exclude(pk=self.instance.pk)
            
            if overlapping_bookings.exists():
                raise forms.ValidationError("Room is already booked for these dates.") 