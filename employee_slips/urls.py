# employee_slips/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_page, name='login_page'),
    path('slip/<str:employee_id>/', views.slip_display_page, name='slip_display_page'),  # URL for displaying the slip 
]