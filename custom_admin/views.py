from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from students.models import StudentsNotes, StudentsTasks, StudentProfile
from django.contrib import messages
from django.db.models import Q
# Create your views here.

def admin_login(request):
    data={}

    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is None:
            data['error_msg'] = "Incorrect Username or Password "
            return render(request, "users/login.html", context=data)

        # Log in the user
        if user.is_superuser:
            login(request, user)
        else:
            messages.error(request, "Not allowed")
            return redirect('/')
            
        return redirect('/custom-admin/dashboard/')

        

    return render(request, "custom_admin/login.html")

def dashboard(request):
    if request.user.is_authenticated:
        data={}
        total_users = User.objects.count()
        data['count_users'] = total_users
    else:
        return redirect('/custom-admin/login')
    return render(request, "custom_admin/dashboard.html", context=data)

def manage_student_profile(request):
    data={}
    course = request.GET.get('course')
    get_student_profiles = StudentProfile.objects.all()
    # data['all_profiles'] = get_student_profiles
    if course:
        get_student_profiles = StudentProfile.objects.filter(course_name__icontains=course)
    
    else:
        get_student_profiles = StudentProfile.objects.all()
    if request.method == "POST":
        query = request.POST.get('search')

        if query:
           get_student_profiles = StudentProfile.objects.filter(Q(user__username__icontains=query) | Q (user__first_name__icontains=query) | Q(user__last_name__icontains=query))
      
    data['all_profiles'] = get_student_profiles


    return render(request, "custom_admin/admin_students/manage_profile.html", context=data)


def studentAddNotes(request):
    data = {}
    getStudents = StudentProfile.objects.all()
    data['students'] = getStudents
    if(request.method == "POST"):
        student_id  = request.POST['studentname']
        notestitle = request.POST['notestitle']
        notesfile = request.FILES.get('notesfile')
        print("=======>", student_id , notestitle, notesfile)
            
        assign_notes = StudentsNotes.objects.create(user_id=student_id , notes_title=notestitle, notes_pdf=notesfile)
        
    return render(request, "custom_admin/admin_students/addNotes.html", context=data)


def studentAssignTask(request):
    data = {}
    getStudents = StudentProfile.objects.all()
    data['students'] = getStudents
    if(request.method == "POST"):
        student_id  = request.POST['studentname']
        task_title = request.POST['task_title']
        task_description = request.POST['description']
            
        assign_task = StudentsTasks.objects.create(user_id=student_id , task_title=task_title, task_description=task_description)
    return render(request, "custom_admin/admin_students/assign_task.html", context=data)

def view_profile_student(request, user_id):
    data={}
    get_user = StudentProfile.objects.get(user_id = user_id)
    data['student'] = get_user
    return render(request, "custom_admin/admin_students/view_profile.html", context=data)

def edit_profile_student(request, user_id):
    data={}
    get_user = StudentProfile.objects.get(user_id = user_id)
    data['student'] = get_user
    return render(request, "custom_admin/admin_students/edit_profile.html", context=data)