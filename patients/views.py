from rest_framework import generics,status
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import PatientProfile
from .serializers import PatientProfileSerializer, PatientProfileCreateSerializer
from accounts.permissions import IsAdmin, IsPatient, IsAdminOrDoctor

class PatientListView(generics.ListAPIView):
    queryset=PatientProfile.objects.select_related('user').all()
    serializer_class=PatientProfileSerializer
    permission_classes=[IsAdminOrDoctor]
    filter_backends=[DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields=[ 'gender', 'blood_group']
    search_fields=['user__first_name', 'user__last_name','user__email']
    ordering_fields=['created_at']
    ordering=['-created_at']
    
    
class PatientDetailView(generics.RetrieveAPIView):
    queryset=PatientProfile.objects.select_related('user').all()
    serializer_class=PatientProfileSerializer
    permission_classes=[IsAdminOrDoctor]
    
    def get_serializer_context(self):
        return {'request': self.request}
    
    
class PatientCreateView(generics.CreateAPIView):
    serializer_class=PatientProfileCreateSerializer
    permission_classes=[IsPatient]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def get_serializer_context(self):
        return {'request': self.request}    

class PatientUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class=PatientProfileCreateSerializer
    permission_classes=[IsAuthenticated]
    
    def get_object(self):
        return PatientProfile.objects.get(user=self.request.user)
    
    def update(self,request, *args, **kwargs):
        kwargs['partial']=True
        return super().update(request, *args, **kwargs)
    
    
class PatientDeleteView(generics.DestroyAPIView):
    queryset=PatientProfile.objects.all()
    permission_classes=[IsAdmin]
    
class MyPatientProfileView(generics.RetrieveAPIView):
    serializer_class=PatientProfileSerializer
    permission_classes=[IsPatient]
    
    def get_object(self):
        return PatientProfile.objects.get(user=self.request.user)
