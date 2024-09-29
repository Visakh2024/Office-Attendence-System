from django.urls import path, include
from .views import CustomLoginView
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'attendance'

urlpatterns = [
    path('', CustomLoginView.as_view(), name='login'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('dashboard/logout', views.logout_view, name='logout'),
    path('check_in/', views.check_in, name='check_in'),
    path('check_out/', views.check_out, name='check_out'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('accounts/', include('django.contrib.auth.urls')),  # Include default auth urls
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
