from django.shortcuts import render
from employee.models import EmployeeProfile
from django.contrib import messages
# Create your views here.
def employeeProfile(request):
    data={}
    try:
        get_employee_data = EmployeeProfile.objects.get(user=request.user)
        data['profile'] = get_employee_data
    except:
        pass
    
    if request.method == "POST":
        phone = request.POST['phone']
        email = request.POST['email']
        education = request.POST['education']
        image = request.FILES['image']
 
        print(image)
        print(phone, email, education)
        # Update the existing User object with the new email    
        user = request.user
        print(user)
        user.email = email
        user.save()
        
        # Update the existing StudentProfile object with new details
        get_employee_data.phone = phone
        get_employee_data.education = education
        get_employee_data.image = image
    
        get_employee_data.save()
        print(get_employee_data.image.url)
        messages.success(request, 'Your profile has been updated successfully.')
    return render(request, 'employee/profile.html', context=data)

def employeeSalary(request):
    data={}
    get_employee_data = EmployeeProfile.objects.get(user=request.user)
    data['salary'] = get_employee_data
    return render(request, "employee/salary.html", context=data)