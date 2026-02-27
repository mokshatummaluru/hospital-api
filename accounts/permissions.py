from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    message="You don't have permission. Admin access required."

    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role=='ADMIN'
        )
        
class IsDoctor(BasePermission):
    message="You don't have permission. Doctor access required."

    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role=='DOCTOR'
        )

class IsPatient(BasePermission):
    message="You don't have permission. Patient access required."
    
    def has_permission(self,request,view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role=='PATIENT'
        )
        
        
class IsReceptionist(BasePermission):
    message="You don't have permission. Receptionist access required."
    
    def has_permission(self,request,view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role=="RECEPTIONIST"
        )
        
class IsAdminOrDoctor(BasePermission):
    message="You do't have permission. Admin or Doctor access required."
    
    def has_permission(self,request,view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role in ['ADMIN', 'DOCTOR']
        )
   
class IsAdminOrReceptionist(BasePermission):
    message="You don't have permission. Admin or Receptionist access required."
    
    def has_permission(self,request,view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role in ['ADMIN', 'RECEPTIONIST']
        )     
        
class IsAdminOrDoctorOrReceptionist(BasePermission):
    message="You don't have permission."
    
    def has_permission(self,request,view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role in ['ADMIN','DOCTOR','RECEPTIONIST']
        )
        
class IsOwnerOrAdmin(BasePermission):
    message="You don't have permission to access this record."
    
    def has_object_permission(self,request,view,obj):
        if(request.user.role=='ADMIN'):
            return True 
        if hasattr(obj,'user'):
            return obj.user == request.user
        
        return obj==request.user