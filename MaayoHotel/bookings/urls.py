from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    # Room URLs
    path('rooms/', views.RoomListView.as_view(), name='room_list'),
    path('room/<int:pk>/', views.RoomDetailView.as_view(), name='room_detail'),
    path('room/create/', views.RoomCreateView.as_view(), name='room_create'),
    path('room/<int:pk>/update/', views.RoomUpdateView.as_view(), name='room_update'),
    path('room/<int:pk>/delete/', views.RoomDeleteView.as_view(), name='room_delete'),

    # Booking URLs
    path('', views.BookingListView.as_view(), name='booking_list'),
    path('booking/<int:pk>/', views.BookingDetailView.as_view(), name='booking_detail'),
    path('booking/create/', views.BookingCreateView.as_view(), name='booking_create'),
    path('booking/<int:pk>/update/', views.BookingUpdateView.as_view(), name='booking_update'),
    path('booking/<int:pk>/delete/', views.BookingDeleteView.as_view(), name='booking_delete'),
] 