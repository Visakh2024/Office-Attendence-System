from django.contrib import admin
from .models import Staff, Attendance

class StaffAdmin(admin.ModelAdmin):
    list_display = ['user', 'position', 'department', 'late_punches', 'half_day_leaves', 'full_day_leaves']
    list_filter = ['position', 'department']
    search_fields = ['user__username']

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['staff', 'date', 'check_in', 'check_out', 'office_start', 'office_end']
    list_filter = ['staff', 'date']
    search_fields = ['staff__user__username']

admin.site.register(Staff, StaffAdmin)
admin.site.register(Attendance, AttendanceAdmin)
