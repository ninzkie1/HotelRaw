from django.contrib import admin
from .models import Room, Booking

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'room_type', 'price', 'is_available')
    list_filter = ('room_type', 'is_available')
    search_fields = ('room_number', 'description')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('guest_name', 'room', 'check_in', 'check_out', 'created_at')
    list_filter = ('check_in', 'check_out', 'room__room_type')
    search_fields = ('guest_name', 'guest_email', 'room__room_number')
    date_hierarchy = 'check_in'
