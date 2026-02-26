from django.contrib import admin
from .models import PatientProfile

@admin.register(PatientProfile)
class PatientProfileAdmin(admin.ModelAdmin):
    list_display=['user', 'gender','blood_group','emergency_contact_name',]
    list_filter=['gender','blood_group']
    search_fields=['user__username', 'user__email']
    
    
    
