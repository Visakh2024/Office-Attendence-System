from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Attendance, Staff
from django.core.files.base import ContentFile
import datetime
import base64
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from .forms import CustomAuthenticationForm

class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'registration/login.html'



@login_required
def dashboard(request):
    staff = Staff.objects.get(user=request.user)
    attendance_records = Attendance.objects.filter(staff=staff)
    return render(request, 'attendance/dashboard.html', {'attendance_records': attendance_records})

@login_required
def check_in(request):
    staff = Staff.objects.get(user=request.user)
    today = datetime.date.today()
    attendance, created = Attendance.objects.get_or_create(staff=staff, date=today)

    if request.method == 'POST':
        photo_data = request.POST.get('photo_data')
        if photo_data:
            attendance.check_in = datetime.datetime.now().time()
            format, imgstr = photo_data.split(';base64,') 
            ext = format.split('/')[-1]
            attendance.check_in_photo.save(f'{staff.user.username}_check_in.{ext}', ContentFile(base64.b64decode(imgstr)), save=False)
            if attendance.is_late_punch():
                staff.increment_late_punches()
            attendance.save()
            return redirect('attendance:dashboard')  # Ensure this is correct

    return render(request, 'attendance/check_in.html')

@login_required
def check_out(request):
    staff = Staff.objects.get(user=request.user)
    today = datetime.date.today()
    try:
        attendance = Attendance.objects.get(staff=staff, date=today)
    except Attendance.DoesNotExist:
        attendance = None

    if attendance and request.method == 'POST':
        photo_data = request.POST.get('photo_data')
        if photo_data:
            attendance.check_out = datetime.datetime.now().time()
            format, imgstr = photo_data.split(';base64,') 
            ext = format.split('/')[-1]
            attendance.check_out_photo.save(f'{staff.user.username}_check_out.{ext}', ContentFile(base64.b64decode(imgstr)), save=False)
            if attendance.is_early_checkout():
                staff.increment_half_day_leaves()
            attendance.save()
            return redirect('attendance:dashboard')

    return render(request, 'attendance/check_out.html')

def logout_view(request):
    logout(request)
    return render(request, 'registration/login.html')
