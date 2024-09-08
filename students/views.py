from django.shortcuts import render
from students.models import StudentProfile, StudentsTasks, StudentsNotes
from django.contrib.auth.models import User
from django.contrib import messages


# Create your views here.
def StudentHome(request):
    return render(request, 'students/profile.html')

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
    try:
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
                get_user_details.phone = phone
                get_user_details.parent_number = parent_number
                get_user_details.education = education
                get_user_details.image = image
            
                get_user_details.save()
                print(get_user_details.image.url)
                messages.success(request, 'Your profile has been updated successfully.')
    except:
        messages.error(request, "All fields are necessary")

    return render(request, "students/profile.html", context=data)

def studentfeesDetails(request):
    data={}
    get_user_fees = StudentProfile.objects.get(user=request.user)
    print(get_user_fees)
    data['fees'] = get_user_fees   
    return render(request, "students/fees.html", context=data)

def StudentTasks(request):
    data = {}
    try:
        # Retrieve all tasks for the logged-in user
        get_user_tasks = StudentsTasks.objects.filter(user=request.user)
        data['tasks'] = get_user_tasks

    except StudentsTasks.DoesNotExist:
        # If no tasks exist, this block will handle the exception
        data['tasks'] = None

    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        assignment_file = request.FILES.get('assignment_file')

        
        # Find the specific task
        task = StudentsTasks.objects.get(id=task_id, user=request.user)

        # Save the uploaded assignment file
        task.assignment = assignment_file
        task.save()

            # messages.success(request, 'Assignment uploaded successfully.')
        # except StudentsTasks.DoesNotExist:
        #     messages.error(request, 'Task not found.')

         # Replace 'tasks_page' with the correct URL name
    return render(request, "students/tasks.html", context=data)

def StudentNotes(request):
    data = {}
    # Retrieve all notes for the logged-in user
 
    get_user_notes = StudentsNotes.objects.filter(user=request.user)
    data['students_notes'] = get_user_notes
    print(get_user_notes)
        
    return render(request, "students/notes.html", context=data)