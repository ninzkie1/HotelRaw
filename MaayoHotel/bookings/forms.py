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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Display only Available rooms sa dropdown
        self.fields['room'].queryset = Room.objects.filter(is_available=True)

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')
        room = cleaned_data.get('room')

        if not room:
            raise forms.ValidationError("Please select a room.")

        # Para dili ma book ang naka false na room is_available
        if not room.is_available:
            raise forms.ValidationError(f"Room {room.room_number} is currently unavailable and cannot be booked.")

        # Para dili mag una ang checking sa past date
        if check_in and check_in < date.today():
            raise forms.ValidationError("Check-in date cannot be in the past.")

        # Og para dapat mag una lang ang check in sa check out date
        if check_in and check_out and check_in >= check_out:
            raise forms.ValidationError("Check-in date must be before check-out date.")

        # dili ka book og room if occupied siya kana na date
        overlapping_bookings = Booking.objects.filter(
            room=room,
            check_in__lt=check_out,
            check_out__gt=check_in
        )

        # kani ig edit para dili ma conflict sa uban existing booking pwede niya ma edit ang booking pero kana avaialble date ra
        if self.instance.pk:
            overlapping_bookings = overlapping_bookings.exclude(pk=self.instance.pk)

        if overlapping_bookings.exists():
            raise forms.ValidationError(f"Room {room.room_number} is already booked for the selected dates.")

        return cleaned_data
