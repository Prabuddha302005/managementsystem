from django.shortcuts import render
from interns.models import InternProfile
from django.contrib import messages

# Create your views here.
def InternHome(request):
    return render(request, 'intern/intern_profile.html')

def internProfile(request):
    data = {}
    
    # Get the student's profile
    try:
        get_intern_details = InternProfile.objects.get(user=request.user)
        data['profile'] = get_intern_details
    except InternProfile.DoesNotExist:
        pass
        # messages.error(request, 'Profile not found.')
        # return redirect('profile_error_page')  # Replace with your error page
    
    if request.method == "POST":
        phone = request.POST['phone']
        parent_number = request.POST['parent_number']
        email = request.POST['email']
        education = request.POST['education']
        image = request.FILES['image']
 
        print(image)
        print(phone, parent_number, email, education)
        # Update the existing User object with the new email
        user = request.user
        print(user)
        user.email = email
        user.save()
        
        # Update the existing StudentProfile object with new details
        get_intern_details.phone = phone
        get_intern_details.parent_number = parent_number
        get_intern_details.education = education
        get_intern_details.image = image
    
        get_intern_details.save()
        print(get_intern_details.image.url)
        messages.success(request, 'Your profile has been updated successfully.')

        # profile image setup    
    return render(request, 'intern/intern_profile.html', context=data)


def internNote(request):
    return render(request, 'intern/notes.html')



def internTask(request):
    return render(request, 'intern/tasks.html')


def internProject(request):
    return render(request, 'intern/projects.html')


def internFees(request):
    return render(request, 'intern/fees.html')