from django.contrib import admin
from uztk.app.models import (
    Camera,
    CameraToTourniquetLock,
    Employee,
    EmployeeGroupTimeSheet,
    EmployeeGroup,
    Location,   
    TourniquetLock,
    TourniquetTimeSheet
)


class CameraAdmin(admin.ModelAdmin):
    list_display = ('id', 'uuid', 'camtype', 'ip_address', 'location', 'created', 'updated')
    
    class Meta:
        model = Camera
        
        
class CameraToTourniquetLockAdmin(admin.ModelAdmin):
    list_display = ('id', 'uuid', 'tourniquet', 'created', 'updated')
    
    class Meta:
        model = CameraToTourniquetLock
    

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'uuid', 'full_name', 'created', 'updated')

    class Meta:
        model = Employee

class EmployeeGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'uuid', 'title', 'created', 'updated')

    class Meta:
        model = EmployeeGroup

class EmployeeGroupTimeSheetAdmin(admin.ModelAdmin):
    list_display = ('id', 'uuid', 'employee_group', 'tourniquet', 'start_time', 'end_time', 'created', 'updated')

    class Meta:
        model = EmployeeGroupTimeSheet

class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'uuid', 'title', 'created', 'updated')
    
    class Meta:
        model = Location
        

class TourniquetLockAdmin(admin.ModelAdmin):
    list_display = ('id', 'uuid', 'lock_type', 'state', 'ip_address', 'location', 'created', 'updated')
    
    class Meta:
        model = TourniquetLock
        
        
class TourniquetTimeSheetAdmin(admin.ModelAdmin):
    list_display = ('id', 'uuid', 'employee', 'tourniquet', 'start_time', 'end_time', 'created', 'updated')
    
    class Meta:
        model = TourniquetTimeSheet


admin.site.register(Camera, CameraAdmin)
admin.site.register(CameraToTourniquetLock, CameraToTourniquetLockAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(EmployeeGroup, EmployeeGroupAdmin)
admin.site.register(EmployeeGroupTimeSheet, EmployeeGroupTimeSheetAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(TourniquetLock, TourniquetLockAdmin)
admin.site.register(TourniquetTimeSheet, TourniquetTimeSheetAdmin)