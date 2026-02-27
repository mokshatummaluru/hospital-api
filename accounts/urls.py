from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from accounts.test_views import AdminOnlyView, AdminOrDoctorView, AdminOrReceptionistView, DoctorOnlyView, PatientOnlyView, ReceptionistOnlyView
from .views import ProfileView, RegisterView, LoginView, LogoutView

urlpatterns = [
    path('register/',RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', ProfileView.as_view(), name='profile'),
    
    
    path('test/admin-only/',AdminOnlyView.as_view(),name='test-admin'),
    path('test/doctor-only/',DoctorOnlyView.as_view(),name='test-doctor'),
    path('test/patient-only/',PatientOnlyView.as_view(),name='test-patient'),
    path('test/receptionist-only/',ReceptionistOnlyView.as_view(),name='test-receptionist'),
    path('test/admin-or-doctor/',AdminOrDoctorView.as_view(),name='test-admin-or-doctor'),
    path('test/admin-or-receptionist/',AdminOrReceptionistView.as_view(),name='test-admin-or-receptionist'),
]
