from django.db import models
from django.contrib.auth.models import User
import datetime


class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    position = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    late_punches = models.IntegerField(default=0)
    half_day_leaves = models.IntegerField(default=0)
    full_day_leaves = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

    def increment_late_punches(self):
        self.late_punches += 1
        if self.late_punches >= 4:
            self.full_day_leaves += 1
            self.late_punches = 0
        self.save()

    def increment_half_day_leaves(self):
        self.half_day_leaves += 1
        self.save()

class Attendance(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    check_in_photo = models.ImageField(upload_to='check_in_photos/', null=True, blank=True)
    check_out_photo = models.ImageField(upload_to='check_out_photos/', null=True, blank=True)
    office_start = models.TimeField(default='09:00:00')
    office_end = models.TimeField(default='17:30:00')

    def __str__(self):
        return f'{self.staff.user.username} - {self.date}'

    def is_late_punch(self):
        return self.check_in and self.check_in > datetime.time(9, 50)

    def is_early_checkout(self):
        return self.check_out and self.check_out < datetime.time(16, 30)
