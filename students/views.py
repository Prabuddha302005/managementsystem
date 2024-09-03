from django.shortcuts import render
from students.models import StudentProfile
from django.contrib.auth.models import User
from django.contrib import messages


# Create your views here.
def StudentHome(request):
    return render(request, 'students/student_home.html')

def studentProfile(request):
    data = {}
    
    # Get the student's profile
    try:
        get_user_details = StudentProfile.objects.get(user=request.user)
        data['profile'] = get_user_details
    except StudentProfile.DoesNotExist:
        pass
        # messages.error(request, 'Profile not found.')
        # return redirect('profile_error_page')  # Replace with your error page
    
    if request.method == "POST":
        phone = request.POST['phone']
        parent_number = request.POST['parent_number']
        email = request.POST['email']
        education = request.POST['education']
        print(phone, parent_number, email, education)
        # Update the existing User object with the new email
        user = request.user
        print(user)
        user.email = email
        user.save()
        
        # Update the existing StudentProfile object with new details
        get_user_details.phone = phone
        get_user_details.parent_number = parent_number
        get_user_details.education = education
        get_user_details.save()
        
        messages.success(request, 'Your profile has been updated successfully.')
        # Redirect to the profile page or another appropriate page

    return render(request, "students/profile.html", context=data)

def studentfeesDetails(request):
    data={}
    get_user_fees = StudentProfile.objects.get(user=request.user)
    print(get_user_fees)
    data['fees'] = get_user_fees   
    return render(request, "students/fees.html", context=data)

