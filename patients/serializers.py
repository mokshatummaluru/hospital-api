from datetime import date
from rest_framework import serializers
from .models import PatientProfile
from accounts.serializers import UserSerializer

class PatientProfileSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    full_name=serializers.SerializerMethodField()
    age=serializers.SerializerMethodField()
    
    class Meta:
        model=PatientProfile
        fields=[
            'id',
            'user',
            'full_name',
            'age',
            'gender',
            'blood_group',
            'height_cm',
            'weight_kg',
            'allergies',
            'chronic_conditions',
            'emergency_contact_name',
            'emergency_contact_phone',
            'insurance_provider',
            'insurance_number',
            'created_at',
            'updated_at',
        ]

        read_only_fields=['id','created_at','updated_at']
    def get_full_name(self,obj):
        return obj.user.get_full_name()

    def get_age(self, obj):
        if(obj.user.date_of_birth):
            today = date.today()
            dob=obj.user.date_of_birth
            return today.year - dob.year -(
                (today.month, today.day) < (dob.month, dob.day)
            )
        return None

class PatientProfileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=PatientProfile
        fields=[
            'gender',
            'blood_group',
            'height_cm',
            'weight_kg',
            'allergies',
            'chronic_conditions',
            'emergency_contact_name',
            'emergency_contact_phone',
            'insurance_provider',
            'insurance_number',
        ]
        def create(self,validated_data):
            user=self.context['request'].user
            if(PatientProfile.objects.filter(user=user).exists()):
                raise serializers.ValidationError(
                    {"error": "Patient profile already exists for this user."}
                )
            return PatientProfile.objects.create(user=user, **validated_data)