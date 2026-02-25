from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        DOCTOR = 'DOCTOR', 'Doctor'
        PATIENT = 'PATIENT', 'Patient'
        RECEPTIONIST = 'RECEPTIONIST', 'Receptionist'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.PATIENT
    )
    phone_number=models.CharField(max_length=15, blank=True, null=True)
    address=models.TextField(blank=True, null=True)
    date_of_birth=models.DateTimeField(blank=True, null=True)
    profile_picture=models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    created_at=models.DateTimeField(auto_now_add=True,null=True)
    updated_at=models.DateTimeField(auto_now=True,null=True)


    def __str__(self):
        return f"{self.username} ({self.role})"
    
    
    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN
    
    @property
    def is_doctor(self):
        return self.role == self.Role.DOCTOR
    
    
    @property
    def is_patient(self):
        return self.role == self.Role.PATIENT

    @property
    def is_receptionist(self):
        return self.role == self.Role.RECEPTIONIST