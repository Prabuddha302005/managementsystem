from django.urls import path
from employee import views

urlpatterns = [
    path('home/', views.employeeHome),
]