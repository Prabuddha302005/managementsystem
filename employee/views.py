from django.shortcuts import render
from employee.models import EmployeeProfile

# Create your views here.
def employeeHome(request):
    return render(request, 'employee/employee_home.html')