from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .permissions import (
    IsAdmin,
    IsDoctor,
    IsPatient,
    IsReceptionist,
    IsAdminOrReceptionist,
    IsAdminOrDoctor,
)

class AdminOnlyView(APIView):
    permission_classes=[IsAdmin]
    
    def get(self,request):
        return Response(
            {"message": f"Hello Admin {request.user.username}! You have full access."},
            status=status.HTTP_200_OK
        )


class DoctorOnlyView(APIView):
    permission_classes=[IsDoctor]
    
    def get(self,request):
        return Response(
            {'message': f"Hello Dr. {request.user.username}! Doctor dashboard."},
            status=status.HTTP_200_OK
        )
        
class PatientOnlyView(APIView):
    permission_classes=[IsPatient]
    
    def get(self,request):
        return Response(
            {'message': f"Hello {request.user.username}!  Patient portal."},
            status=status.HTTP_200_OK
        )
        
class ReceptionistOnlyView(APIView):
    permission_classes=[IsReceptionist]
    
    def get(self,request):
        return Response(
            {'message': f"Hello {request.user.username}! Receptionist dashboard."},
            status=status.HTTP_200_OK
        )
        
class AdminOrDoctorView(APIView):
    permission_classes=[IsAdminOrDoctor]
    
    def get(self,request):
        return Response(
            {'message':f"Hello {request.user.username}! You are {request.user.role}. Access granted"},
            status=status.HTTP_200_OK 
        )
        
class AdminOrReceptionistView(APIView):
    permission_classes=[IsAdminOrReceptionist]
    
    def get(self,request):
        return Response(
            {'message':f"Hello {request.user.username}! You are {request.user.role}. Access granted"},
            status=status.HTTP_200_OK 
        )
        
        
