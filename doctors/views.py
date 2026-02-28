from rest_framework import generics,status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework  import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import DoctorProfile
from .serializers import DoctorProfileSerializer, DoctorProfileCreateSerializer
from accounts.permissions import IsAdmin, IsDoctor, IsAdminOrDoctor

class DoctorListView(generics.ListAPIView):
    queryset=DoctorProfile.objects.select_related('user').all()
    serializer_class=DoctorProfileSerializer
    permission_classes=[IsAuthenticated]
    filter_backends=[DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields=['specialization', 'is_available']
    search_fields=['user__first_name', 'user__last_name', 'specialization']
    ordering_fields=['consultation_fee', 'years_of_experience']
    ordering=['user__first_name']
    
class DoctorDetailView(generics.RetrieveAPIView):
    queryset=DoctorProfile.objects.select_related('user').all()
    serializer_class=DoctorProfileSerializer
    permission_classes=[IsAuthenticated]
    
class DoctorCreateView(generics.CreateAPIView):
    serializer_class=DoctorProfileCreateSerializer
    permission_classes=[IsDoctor]
    def get_serializer_context(self):
        return {'request': self.request}
    
    
class DoctorUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class=DoctorProfileCreateSerializer
    permission_classes=[IsAdminOrDoctor]
    
    def get_object(self):
        return DoctorProfile.objects.get(user=self.request.user)
    
    
    def update(self,request, *args, **kwargs):
        kwargs['partial']=True
        return super().update(request, *args, **kwargs)
    
    
class DoctorDeleteView(generics.DestroyAPIView):
    queryset=DoctorProfile.objects.all()
    permission_classes=[IsAdmin]
    
    