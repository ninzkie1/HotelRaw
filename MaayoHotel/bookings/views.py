from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Room, Booking
from .forms import RoomForm, BookingForm

# Create your views here.

# Room Views
class RoomListView(ListView):
    model = Room
    template_name = 'bookings/room_list.html'
    context_object_name = 'rooms'

class RoomDetailView(DetailView):
    model = Room
    template_name = 'bookings/room_detail.html'
    context_object_name = 'room'

class RoomCreateView(CreateView):
    model = Room
    form_class = RoomForm
    template_name = 'bookings/room_form.html'
    success_url = reverse_lazy('bookings:room_list')

    def form_valid(self, form):
        messages.success(self.request, 'Room created successfully!')
        return super().form_valid(form)

class RoomUpdateView(UpdateView):
    model = Room
    form_class = RoomForm
    template_name = 'bookings/room_form.html'
    success_url = reverse_lazy('bookings:room_list')

    def form_valid(self, form):
        messages.success(self.request, 'Room updated successfully!')
        return super().form_valid(form)

class RoomDeleteView(DeleteView):
    model = Room
    template_name = 'bookings/room_confirm_delete.html'
    success_url = reverse_lazy('bookings:room_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Room deleted successfully!')
        return super().delete(request, *args, **kwargs)

# Booking Views
class BookingListView(ListView):
    model = Booking
    template_name = 'bookings/booking_list.html'
    context_object_name = 'bookings'
    ordering = ['-created_at']

class BookingDetailView(DetailView):
    model = Booking
    template_name = 'bookings/booking_detail.html'
    context_object_name = 'booking'

class BookingCreateView(CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'bookings/booking_form.html'
    success_url = reverse_lazy('bookings:booking_list')

    def form_valid(self, form):
        messages.success(self.request, 'Booking created successfully!')
        return super().form_valid(form)

class BookingUpdateView(UpdateView):
    model = Booking
    form_class = BookingForm
    template_name = 'bookings/booking_form.html'
    success_url = reverse_lazy('bookings:booking_list')

    def form_valid(self, form):
        messages.success(self.request, 'Booking updated successfully!')
        return super().form_valid(form)

class BookingDeleteView(DeleteView):
    model = Booking
    template_name = 'bookings/booking_confirm_delete.html'
    success_url = reverse_lazy('bookings:booking_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Booking deleted successfully!')
        return super().delete(request, *args, **kwargs)
