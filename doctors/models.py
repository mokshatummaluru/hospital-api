from django.db import models
from accounts.models import User

class DoctorProfile(models.Model):
    class Specialization(models.TextChoices):
        GENERAL='GENERAL','General Physician'
        CARDIOLOGY='CARDIOLOGY','Cardiology'
        NEUROLOGY='NEUROLOGY','Neurology'
        ORTHOPEDICS='ORTHOPEDICS','Orthopedics'
        PEDIATRICS='PEDIATRICS','Pediatrics'
        DERMATOLOGY='DERMATOLOGY','Dermatology'
        PSYCHIATRY='PSYCHIATRY','Psychiatry'
        GYNECOLOGY='GYNECOLOGY','Gynecology'
        ONCOLOGY='ONCOLOGY','Oncology'
        RADIOLOGY='RADIOLOGY','Radiology'
        
    user=models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='doctor_profile'
    )
    specialization=models.CharField(
        max_length=50,
        choices=Specialization.choices,
        default=Specialization.GENERAL
    )
    license_number=models.CharField(max_length=100, unique=True)
    years_of_experience=models.PositiveIntegerField(default=0)
    consultation_fee=models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    available_from=models.TimeField(blank=True, null=True)
    available_to=models.TimeField(blank=True, null=True)
    available_days=models.JSONField(default=list)
    bio=models.TextField(blank=True,null=True)
    is_available=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True,null=True)
    updated_at=models.DateTimeField(auto_now=True,null=True)

    def __str__(self):
        return f"Dr. {self.user.get_full_name()} - {self.specialization}"
    