from django.db import models
from accounts.models import User

class PatientProfile(models.Model):
    class BloodGroup(models.TextChoices):
        A_POS='A+','A+'
        A_NEG='A-','A-'
        B_POS='B+','B+'
        B_NEG='B-','B-'
        AB_POS='AB+','AB+'
        AB_NEG='AB-','AB-'
        O_POS='O+','O+'
        O_NEG='O-','O-'
        
    class Gender(models.TextChoices):
        MALE='MALE','Male',
        FEMALE='FEMALE','Female',
        OTHER='OTHER','Other'
        
    user=models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='patient_profile'
    )
    
    gender=models.CharField(
        max_length=10,
        choices=Gender.choices,
        blank=True,
        null=True
    )
    
    blood_group=models.CharField(
        max_length=5,
        choices=BloodGroup.choices,
        blank=True,
        null=True
    )
    height_cm=models.FloatField(blank=True, null=True)
    weight_kg=models.FloatField(blank=True, null=True)
    allergies=models.TextField(blank=True, null=True)
    chronic_conditions=models.TextField(blank=True, null=True)
    emergency_contact_name=models.CharField(max_length=100, blank=True, null=True)
    emergency_contact_phone=models.CharField(max_length=15, blank=True, null=True)
    insurance_provider=models.CharField(max_length=100, blank=True, null=True)
    insurance_number=models.CharField(max_length=100, blank=True, null=True)
    created_at=models.DateTimeField(auto_now_add=True,null=True)
    updated_at=models.DateTimeField(auto_now=True,null=True)
    
    
    def __str__(self):
        return f"{self.user.get_full_name()} - Patient"
    
    
