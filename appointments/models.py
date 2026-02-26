from django.db import models
from accounts.models import User
from doctors.models import DoctorProfile
from patients.models import PatientProfile

class Appointment(models.Model):
    class Status(models.TextChoices):
        PENDING='PENDING','Pending',
        CONFIRMED='CONFIRMED','Confirmed',
        CANCELLED='CANCELLED','Cancelled',
        COMPLETED='COMPLETED','Completed'
        NO_SHOW='NO_SHOW','No Show'
        
    class AppointmentType(models.TextChoices):
        IN_PERSON='IN_PERSON','In Person',
        ONLINE='ONLINE','Online'
        
    patient=models.ForeignKey(
        PatientProfile,
        on_delete=models.CASCADE,
        related_name='appointments'
    )
    
    doctor=models.ForeignKey(
        DoctorProfile,
        on_delete=models.CASCADE,
        related_name='appointments'
    )

    booked_by=models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='booked_appointments'
    )
    
    appointment_date=models.DateTimeField()
    appointment_time=models.TimeField()
    appointment_type=models.CharField(
        max_length=20,
        choices=AppointmentType.choices,
        default=AppointmentType.IN_PERSON
    )
    status=models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    reason=models.TextField(blank=True, null=True)
    symptoms=models.TextField(blank=True, null=True)
    doctor_notes=models.TextField(blank=True, null=True)
    prescription=models.TextField(blank=True, null=True)
    follow_up_date=models.DateTimeField(blank=True, null=True)
    created_at=models.DateTimeField(auto_now_add=True,null=True)
    updated_at=models.DateTimeField(auto_now=True,null=True)
    
    class Meta:
        ordering=['-appointment_date','-appointment_time']
        unique_together=['doctor','appointment_date','appointment_time']
        
        
    def __str__(self):
        return f"{self.patient} with Dr. {self.doctor} on {self.appointment_date} at {self.appointment_time}"
    
