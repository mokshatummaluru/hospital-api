from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.exceptions import PermissionDenied
from .models import Appointment
from .serializers import AppointmentSerializer,AppointmentCreateSerializer, AppointmentUpdateSerializer
from accounts.permissions import IsAdmin, IsDoctor, IsPatient, IsAdminOrDoctor, IsAdminOrReceptionist, IsAdminOrDoctorOrReceptionist


class AppointmentListView(generics.ListAPIView):
    serializer_class=AppointmentSerializer
    permission_classes=[IsAdminOrReceptionist]
    filter_backends=[DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields=['status', 'appointment_type', 'appointment_date']
    search_fields=[
        'patient__user__first_name',
        'patient__user__last_name',
        'status',
    ]
    ordering_fields=['appointment_date','appointment_time', 'created_at']
    ordering=['-appointment_date']
    
    def get_queryset(self):
        return Appointment.objects.select_related(
            'patient__user',
            'doctor__user',
            'booked_by',
        ).all()
        
        
class AppointmentCreateView(generics.CreateAPIView):
    serializer_class=AppointmentCreateSerializer
    permission_classes=[IsAuthenticated]
    
    def get_serializer_context(self):
        return {'request': self.request}
    
    
    
class AppointmentDetailView(generics.RetrieveAPIView):
    serializer_classes=AppointmentSerializer
    permission_classes=[IsAdminOrDoctorOrReceptionist]
    def get_queryset(self):
        return Appointment.objects.select_related(
            'patient__user',
            'doctor__user',
            'booked_by',
        ).all()
        
class AppointmentUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class=AppointmentUpdateSerializer
    permission_classes=[IsAdminOrDoctor]
    
    def get_queryset(self):
        user = self.request.user

        if user.role == "ADMIN":
            return Appointment.objects.all()

        if user.role == "DOCTOR":
            return Appointment.objects.filter(doctor__user=user)
        raise PermissionDenied("You do not have permission.")
    
    def update(self,request, *args, **kwargs):
        kwargs['partial']=True
        return super().update(request, *args, **kwargs)


class AppointmentCancelView(APIView):
    permission_classes=[IsAuthenticated]
    
    def post(self,request,pk):
        try:
            appointment=Appointment.objects.get(pk=pk)
        except Appointment.DoesNotExist:
            return Response(
                {"error": "Appointment not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if (request.user.role=='PATIENT'):
            if (appointment.patient.user!=request.user):
                return Response(
                    {"error": "You can only cancel your own appointments"},
                    status=status.HTTP_403_FORBIDDEN
                )


        if(appointment.status=='CANCELLED'):
            return Response(
                {"error": "Appointment is already cancelled."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        if(appointment.status=='COMPLETED'):
            return Response(
                {"error": "Cannot cancel a completed appointment."},
                status=status.HTTP_400_BAD_REQUEST
            )
        appointment.status='CANCELLED'
        appointment.save()
        return Response(
            {"message": "Appointment cancelled successfully."},
            status=status.HTTP_200_OK
        )

class MyAppointmentsView(generics.ListAPIView):
    serializer_class=AppointmentSerializer
    permission_classes=[IsAuthenticated]
    filter_backends=[DjangoFilterBackend, OrderingFilter]
    filterset_fields=['status', 'appointment_date']
    ordering=['-appointment_date']
    
    
    def get_queryset(self):
        user=self.request.user
        if(user.role=="DOCTOR"):
            return Appointment.objects.select_related(
                'patient__user',
                'doctor__user',
            ).filter(doctor__user=user)
        elif(user.role=="PATIENT"):
            return Appointment.objects.select_related(
                'patient__user',
                'doctor__user',
            ).filter(patient__user=user)
        return Appointment.objects.none()    