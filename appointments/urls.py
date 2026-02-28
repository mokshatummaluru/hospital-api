from django.urls import path
from .views import (
    AppointmentListView,
    AppointmentDetailView,
    AppointmentCreateView,
    AppointmentUpdateView,
    AppointmentCancelView,
    MyAppointmentsView
)

urlpatterns = [
    path('', AppointmentListView.as_view(), name='appointment-list'),
    path('<int:pk>/', AppointmentDetailView.as_view(), name='appointment-detail'),
    path('create/', AppointmentCreateView.as_view(), name='appointment-create'),
    path('<int:pk>/update/', AppointmentUpdateView.as_view(), name='appointment-update'),
    path('<int:pk>/cancel/', AppointmentCancelView.as_view(), name='appointment-cancel'),
    path('my-appointments/', MyAppointmentsView.as_view(), name='my-appointments'),
]
