from django.urls import path
from .views import (
    PatientListView,
    PatientDetailView,
    PatientCreateView,
    PatientUpdateView,
    PatientDeleteView,
    MyPatientProfileView
 )

urlpatterns = [
    path('', PatientListView.as_view(), name='patient-list'),
    path('<int:pk>/', PatientDetailView.as_view(), name='patient-detail'),
    path('create/', PatientCreateView.as_view(), name='patient-create'),
    path('my-profile/', MyPatientProfileView.as_view(), name='patient-my-profile'),
    path('<int:pk>/delete/', PatientDeleteView.as_view(), name='patient-delete'),
]