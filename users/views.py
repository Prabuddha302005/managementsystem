from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from employee.models import EmployeeProfile
from interns.models import InternProfile
from students.models import StudentProfile
# Create your views here.

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is None:
            # Optionally handle invalid credentials
            print("Wrong Password")
            return render(request, "users/login.html")

        # Log in the user
        login(request, user)

        # Check for different profiles
        try:
            # Check for EmployeeProfile
            employee_profile = EmployeeProfile.objects.get(user=user)
            if employee_profile.role == "Employee":
                return redirect('/employee/home')
        except EmployeeProfile.DoesNotExist:
            pass  # Handle the case if EmployeeProfile does not exist

        try:
            # Check for InternProfile
            intern_profile = InternProfile.objects.get(user=user)
            if intern_profile.role == "Intern":
                return redirect('/intern')
        except InternProfile.DoesNotExist:
            pass  # Handle the case if InternProfile does not exist

        try:
            # Check for StudentProfile
            student_profile = StudentProfile.objects.get(user=user)
            if student_profile.role == "Student":
                return redirect('/student/home')
        except StudentProfile.DoesNotExist:
            pass  # Handle the case if StudentProfile does not exist

        # Redirect to a default page or show an error if no profile matches
        return redirect('/default_page')  # Adjust as needed

    return render(request, 'users/login.html')




# def home(request):
#     if(request.user.is_authenticated):
#         return render(request, "users/home.html")
#     else:
#         return redirect("/")
#   return render(request, "users/home.html")

def user_logout(request):
    logout(request)
    return redirect('/')


