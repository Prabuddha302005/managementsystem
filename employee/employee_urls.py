from django.urls import path
from employee import views

urlpatterns = [
    path('profile/', views.employeeProfile),
    path('salary/', views.employeeSalary),
]