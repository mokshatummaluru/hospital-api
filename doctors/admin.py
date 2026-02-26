from django.contrib import admin
from .models import DoctorProfile


@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display=['user','specialization','license_number','years_of_experience','is_available']
    list_filter=['specialization','is_available']
    search_fields=['user__username', 'user__email', 'license_number']
    
    
