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

def addUser(request):
    data = {}
    if(request.method == "POST"):
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if(username =="" or email == "" or password1 == "" or password2 == ""):
            messages.error(request, "All fileds are necessary")
        elif(password1 != password2):
            messages.error(request, "Password doesn't match")
        elif(User.objects.filter(username=username).exists()):
            messages.error(request, "Username already exists")
        else:
            user = User.objects.create(username=username, email=email)
            user.set_password(password1)
            user.save()
            messages.success(request, "User Created successfully")
    return render(request, "custom_admin/add_user.html", context=data)


def add_student_profile(request):
    data = {}
    get_users = User.objects.all()
    data['users'] = get_users

    if request.method == "POST":
        username = request.POST['username']
        course_name = request.POST['course_name']
        remark = request.POST['remark']
        total_fees = request.POST['total_fees']
        print(username, course_name, remark, total_fees)
        if(StudentProfile.objects.filter(user_id=username).exists()):
            messages.error(request, "Student Profile already exists")
        else:

            save_profile = StudentProfile.objects.create(user_id=username, course_name=course_name, remark=remark, total_fees=total_fees)

            messages.success(request, "Profile created sucessfully.")
    return render(request, "custom_admin/admin_students/add_profile_student.html", context=data)

# def add_intern_profile(request):
# ---- for interns profile. 
#     data = {}
#     get_users = User.objects.all()
#     data['users'] = get_users

#     if request.method == "POST":
#         username = request.POST['username']
#         internship_name = request.POST['internship_name']
#         remark = request.POST['remark']
#         total_fees = request.POST['total_fees']
#         print(username, internship_name, remark, total_fees)
#         if(StudentProfile.objects.filter(user_id=username).exists()):
#             messages.error(request, "Student Profile already exists")
#         else:

#             save_profile = StudentProfile.objects.create(user_id=username, course_name=course_name, remark=remark, total_fees=total_fees)

#             messages.success(request, "Profile created sucessfully.")
#     return render(request, "custom_admin/admin_students/add_profile_student.html", context=data)
    
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

def studentAssignTaskCheck(request):
    data = {}
    
    # Get search query from the request
    search_query = request.GET.get('search', '')
    
    # Filter tasks by search query (student username or task title)
    if search_query:
        tasks = StudentsTasks.objects.filter(
            Q(user__username__icontains=search_query) | 
            Q(task_title__icontains=search_query)
        )
    else:
        tasks = StudentsTasks.objects.all()  # If no search, return all tasks
    
    # Add the tasks to the context
    data['tasks'] = tasks

    return render(request, "custom_admin/admin_students/check_tasks_student.html", context=data)

def view_profile_student(request, user_id):
    data={}
    get_user = StudentProfile.objects.get(user_id = user_id)
    data['student'] = get_user
    return render(request, "custom_admin/admin_students/view_profile.html", context=data)

def edit_profile_student(request, user_id):
    data={}
    try:
        get_user_profile = StudentProfile.objects.get(user_id = user_id)
        get_user = User.objects.get(id=user_id)
        data['student'] = get_user_profile


        if(request.method=="POST"):
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            phone = request.POST['phone']
            parent_number = request.POST['parent_number']
            course_name = request.POST['course_name']

            get_user.first_name = first_name
            get_user.last_name = last_name
            get_user_profile.phone = phone
            get_user_profile.parent_number = parent_number
            get_user_profile.course_name = course_name
            get_user.save()
            get_user.save()
            messages.success(request, "Data saved ")
    except:
         messages.error(request, "error occurred ")


        
    return render(request, "custom_admin/admin_students/edit_profile.html", context=data)