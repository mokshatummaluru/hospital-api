from django.urls import path
from .views import (
    DoctorListView,
    DoctorDetailView,
    DoctorCreateView,
    DoctorUpdateView,
    DoctorDeleteView
)

urlpatterns = [
    path('', DoctorListView.as_view(), name='doctor-list'),
    path('<int:pk>/', DoctorDetailView.as_view(), name='doctor-detail'),
    path('create/', DoctorCreateView.as_view(), name='doctor-create'),
    path('my-profile/', DoctorUpdateView.as_view(), name='doctor-my-profile'),
    path('<int:pk>/delete/', DoctorDeleteView.as_view(), name='doctor-delete'),
]