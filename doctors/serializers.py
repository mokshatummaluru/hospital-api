from rest_framework import serializers
from .models import DoctorProfile
from accounts.serializers import UserSerializer

class DoctorProfileSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    full_name=serializers.SerializerMethodField()
    
    class Meta:
        model=DoctorProfile
        fields=[
            'id',
            'user',
            'full_name',
            'specialization',
            'license_number',
            'years_of_experience',
            'available_from',
            'available_to',
            'available_days',
            'bio',
            'is_available',
            'created_at',
            'updated_at',
        ]
        read_only_fields=['id','created_at','updated_at']
        
    def get_full_name(self,obj):
        return obj.user.get_full_name()


class DoctorProfileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=DoctorProfile
        fields=[
            'specialization',
            'license_number',
            'years_of_experience',
            'consultation_fee',
            'available_from',
            'available_to',
            'available_days',
            'bio',
            'is_available',
        ]
        
    def create(self,validated_data):
        user=self.context['request'].user
        if(DoctorProfile.objects.filter(user=user).exists()):
            raise serializers.ValidationError(
                {"error": "Doctor profile already exists for this user."}
            )
        return DoctorProfile.objects.create(user=user, **validated_data)