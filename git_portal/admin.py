from django.contrib import admin
from .models import *


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['Name', 'Leave_Balance', 'CF_LB']
    list_filter = ['Leave_Balance', 'CF_LB']


class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['Date', 'User', 'Value']
    list_filter = ['Date' , 'User', 'Value']


class DateAdmin(admin.ModelAdmin):
    list_display = ['My_Date', 'all_presence', 'get_attendances']


admin.site.register(Date, DateAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Attendance, AttendanceAdmin)






# class EmployeeAdmin(admin.ModelAdmin):
#     list_display = ['Name', ]
#
#
# class AttendanceAdmin(admin.ModelAdmin):
#     list_display = ['AtDate', ]
#
#
# class AtMonthAdmin(admin.ModelAdmin):
#     list_display = ['Name', ]
#
#
# admin.site.register(Employee, EmployeeAdmin)
# admin.site.register(Attendance, AttendanceAdmin)
# admin.site.register(AtMonth, AtMonthAdmin)
#
