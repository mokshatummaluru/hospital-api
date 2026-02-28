import datetime
from rest_framework import serializers

from patients.models import PatientProfile
from .models import Appointment
from doctors.serializers import DoctorProfileSerializer
from patients.serializers import PatientProfileSerializer
from datetime import date


class AppointmentSerializer(serializers.ModelSerializer):
    doctor=DoctorProfileSerializer(read_only=True)
    patient=PatientProfileSerializer(read_only=True)
    booked_by_username=serializers.SerializerMethodField()

    class Meta:
        model=Appointment
        fields=[
            'id',
            'doctor',
            'patient',
            'booked_by_username',
            'appointment_time',
            'appointment_date',
            'status',
            'reason',
            'symptoms',
            'doctor_notes',
            'prescription',
            'follow_up_date',
            'created_at',
            'updated_at',
        ]

        read_only_fields=['id','created_at','updated_at']

    def get_booked_by_username(self,obj):
        return obj.booked_by.username if obj.booked_by else None
    
    
class AppointmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Appointment
        fields=[
            'doctor',
            'appointment_time',
            'appointment_date',
            'appointment_type',
            'reason',
            'symptoms',
        ]

    def validate_appointment_date(self, value):
        if hasattr(value, "date"):
            value = value.date()

        if value < date.today():
            raise serializers.ValidationError("Appointment date cannot be in the past.")
        return value
    
    def validate(self,attrs):
        doctor=attrs.get('doctor')
        appointment_date=attrs.get('appointment_date')
        appointment_time=attrs.get('appointment_time')

        if (Appointment.objects.filter(
            doctor=doctor,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
        ).exists()):
            raise serializers.ValidationError(
                {"error": "this time slot is already booked for the selected doctor."}
                
            )
        return attrs
    
    def create(self,validated_data):
        user=self.context['request'].user
        patient_profile = PatientProfile.objects.get(user=user)
        return Appointment.objects.create(
            booked_by=user,
            patient=patient_profile,
            **validated_data
        )
            
            
class AppointmentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Appointment
        fields=[
            
            'status',
            'doctor_notes',
            'prescription',
            'follow_up_date',
        ]
