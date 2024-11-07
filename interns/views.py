from django.shortcuts import render, redirect
from interns.models import InternProfile, InternTasks, InternNotes, InternProject, FeesIntern
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
    data = {}
    # Retrieve all notes for the logged-in user
 
    get_user_notes = InternNotes.objects.filter(user=request.user)
    data['students_notes'] = get_user_notes
    print(get_user_notes)
    return render(request, 'intern/notes.html', context=data)



def internTask(request):
    data = {}
    try:
        # Retrieve all tasks for the logged-in user
        get_intern_tasks = InternTasks.objects.filter(user=request.user)
        data['tasks'] = get_intern_tasks

    except InternTasks.DoesNotExist:
        # If no tasks exist, this block will handle the exception
        data['tasks'] = None

    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        assignment_file = request.FILES.get('assignment_file')

        
        # Find the specific task
        task = InternTasks.objects.get(id=task_id, user=request.user)

        # Save the uploaded assignment file
        task.assignment = assignment_file
        task.save()

            # messages.success(request, 'Assignment uploaded successfully.')
        # except StudentsTasks.DoesNotExist:
        #     messages.error(request, 'Task not found.')

         # Replace 'tasks_page' with the correct URL name
    return render(request, 'intern/tasks.html', context=data)


def internProject(request):
    data={}
    user_projects = InternProject.objects.filter(user=request.user)
    data['projects'] = user_projects


    if request.method == "POST":
        project_id = request.POST.get('project_id')
        assignment_file = request.FILES.get('assignment_file')
        project_link = request.POST.get('project_link')

        print(project_id, assignment_file, project_link)
        # Find the specific task
        project = InternProject.objects.get(id=project_id, user=request.user)

        # Save the uploaded assignment file
        project.project_file = assignment_file
        project.project_link = project_link
        project.save()

    return render(request, 'intern/projects.html', context=data)


def internFees(request):
    data={}
    get_intern_fees = FeesIntern.objects.filter(intern_profile_id__user=request.user).last()
    print(get_intern_fees)
    data['fees'] = get_intern_fees   
    return render(request, 'intern/fees.html', context=data)