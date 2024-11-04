from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from students.models import StudentsNotes, StudentsTasks, StudentProfile, Fees
from interns.models import InternProfile, InternNotes, InternProject, FeesIntern, InternTasks
from employee.models import EmployeeProfile
from django.contrib import messages
from django.db.models import Q
from django.conf import settings
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
        paid_fees = request.POST['paid_fees']
        pending_fees = request.POST['pending_fees']
        fees_remark = request.POST['fees_remark']
        if(StudentProfile.objects.filter(user_id=username).exists()):
            messages.error(request, "Student Profile already exists")
        else:

            save_profile = StudentProfile.objects.create(user_id=username, course_name=course_name, remark=remark)

            Fees.objects.create(
                student_profile=save_profile,  # Link to the student profile instance
                total_fees=total_fees,
                paid_fees=paid_fees,
                pending_fees=pending_fees,  # Automatically calculated
                fees_remark=fees_remark
            )
            messages.success(request, "Profile created sucessfully.")
    return render(request, "custom_admin/admin_students/add_profile_student.html", context=data)

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

def update_student_fees(request, user_id):
    user = get_object_or_404(User, id=user_id)
    last_fee_record = Fees.objects.filter(student_profile__user=user).order_by('-id').first()
    
    if request.method == "POST":
        # Retrieve last total fees and new payment amount
        total_fees = last_fee_record.total_fees if last_fee_record else 0
        paid_fees = int(request.POST.get("paid_fees", 0))
        fees_remark = request.POST.get("fees_remark", "")

        # Calculate new cumulative paid amount
        total_paid_so_far = last_fee_record.paid_fees if last_fee_record else 0
        new_total_paid = total_paid_so_far + paid_fees

        # Calculate pending fees based on total fees
        new_pending_fees = total_fees - new_total_paid

        # Get the student profile and save the updated fees data
        student_profile = get_object_or_404(StudentProfile, user=user)
        Fees.objects.create(
            student_profile=student_profile,
            total_fees=total_fees,
            paid_fees=new_total_paid,
            pending_fees=new_pending_fees,
            fees_remark=fees_remark
        )

        # Display a success message
        messages.success(request, "Payment successfully added and fees updated.")
        return redirect('fees_list')  # Redirect to the fees list or appropriate page

    # Pass data to the template for display
    data = {
        'user': user,
        'last_total_fees': last_fee_record.total_fees if last_fee_record else '',
        'last_pending_fees': last_fee_record.pending_fees if last_fee_record else '',
    }
    return render(request, "custom_admin/admin_students/update_fees.html", context=data)

def student_fees_history(request, user_id):
    # Get the user object
    user = get_object_or_404(User, id=user_id)

    # Fetch fees associated with this user
    fees_records = Fees.objects.filter(student_profile__user=user)

    # Pass the records to the context
    context = {
        'user': user,
        'fees_records': fees_records
    }
    return render(request, "custom_admin/admin_students/fees_history.html", context)


# interns
def add_intern_profile(request):
    data = {}
    get_users = User.objects.all()
    data['users'] = get_users

    if request.method == "POST":
        username = request.POST['username']
        internship_name = request.POST['internship_name']
        remark = request.POST['remark']
        total_fees = request.POST['total_fees']
        paid_fees = request.POST['paid_fees']
        pending_fees = request.POST['pending_fees']
        fees_remark = request.POST['fees_remark']
        if(InternProfile.objects.filter(user_id=username).exists()):
            messages.error(request, "Intern Profile already exists")
        else:

            save_profile = InternProfile.objects.create(user_id=username, internship_name=internship_name, remark=remark)

            FeesIntern.objects.create(
                intern_profile=save_profile,  # Link to the intern profile instance
                total_fees=total_fees,
                paid_fees=paid_fees,
                pending_fees=pending_fees,  # Automatically calculated
                fees_remark=fees_remark
            )
            messages.success(request, "Profile created sucessfully.")
    return render(request, "custom_admin/admin_interns/add_profile_intern.html", context=data)

def manage_interns_profile(request):
    data={}
    course = request.GET.get('course')
    get_intern_profiles = InternProfile.objects.all()
    if course:
        get_intern_profiles = InternProfile.objects.filter(internship_name__icontains=course)
    
    else:
        get_intern_profiles = InternProfile.objects.all()
    if request.method == "POST":
        query = request.POST.get('search')

        if query:
           get_intern_profiles = InternProfile.objects.filter(Q(user__username__icontains=query) | Q (user__first_name__icontains=query) | Q(user__last_name__icontains=query))
      
    data['all_profiles'] = get_intern_profiles
    return render(request, "custom_admin/admin_interns/manage_profile.html", context=data)

def view_profile_intern(request, user_id):
    data={}
    get_user = InternProfile.objects.get(user_id = user_id)
    data['intern'] = get_user
    
    return render(request, "custom_admin/admin_interns/view_profile.html", context=data)

def edit_profile_intern(request, user_id):
    data={}
    try:
        get_user_profile = InternProfile.objects.get(user_id = user_id)
        get_user = User.objects.get(id=user_id)
        data['intern'] = get_user_profile


        if(request.method=="POST"):
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            phone = request.POST['phone']
            parent_number = request.POST['parent_number']
            internship_name = request.POST['internship_name']

            get_user.first_name = first_name
            get_user.last_name = last_name
            get_user_profile.phone = phone
            get_user_profile.parent_number = parent_number
            get_user_profile.internship_name = internship_name
            get_user.save()
            get_user.save()
            messages.success(request, "Data saved")
    except:
         messages.error(request, "error occurred ")
       
    return render(request, "custom_admin/admin_interns/edit_profile_intern.html", context=data)

def update_intern_fees(request, user_id):
    user = get_object_or_404(User, id=user_id)
    last_fee_record = FeesIntern.objects.filter(intern_profile__user=user).order_by('-id').first()
    
    if request.method == "POST":
        # Retrieve last total fees and new payment amount
        total_fees = last_fee_record.total_fees if last_fee_record else 0
        paid_fees = int(request.POST.get("paid_fees", 0))
        fees_remark = request.POST.get("fees_remark", "")

        # Calculate new cumulative paid amount
        total_paid_so_far = last_fee_record.paid_fees if last_fee_record else 0
        new_total_paid = total_paid_so_far + paid_fees

        # Calculate pending fees based on total fees
        new_pending_fees = total_fees - new_total_paid

        # Get the student profile and save the updated fees data
        intern_profile = get_object_or_404(InternProfile, user=user)
        FeesIntern.objects.create(
            intern_profile=intern_profile,
            total_fees=total_fees,
            paid_fees=new_total_paid,
            pending_fees=new_pending_fees,
            fees_remark=fees_remark
        )

        # Display a success message
        messages.success(request, "Payment successfully added and fees updated.")
        return redirect('fees_list')  # Redirect to the fees list or appropriate page

    # Pass data to the template for display
    data = {
        'user': user,
        'last_total_fees': last_fee_record.total_fees if last_fee_record else '',
        'last_pending_fees': last_fee_record.pending_fees if last_fee_record else '',
    }
    return render(request, "custom_admin/admin_interns/update_fees.html", context=data)

def intern_fees_history(request, user_id):
    # Get the user object
    user = get_object_or_404(User, id=user_id)

    # Fetch fees associated with this user
    fees_records = FeesIntern.objects.filter(intern_profile__user=user)

    # Pass the records to the context
    context = {
        'user': user,
        'fees_records': fees_records
    }
    return render(request, "custom_admin/admin_interns/fees_history.html", context)

def internAddNotes(request):
    data = {}
    getIntern = InternProfile.objects.all()
    data['interns'] = getIntern
    if(request.method == "POST"):
        intern_id  = request.POST['intername']
        notestitle = request.POST['notestitle']
        notesfile = request.FILES.get('notesfile')
        print("=======>", intern_id , notestitle, notesfile)
            
        assign_notes = InternNotes.objects.create(user_id=intern_id , notes_title=notestitle, notes_pdf=notesfile)
    return render(request, "custom_admin/admin_interns/add_notes.html", context=data)

def internAssignProject(request):
    data = {}
    getInterns = InternProfile.objects.all()
    data['interns'] = getInterns
    if(request.method == "POST"):
        intern_id  = request.POST['internname']
        project_title = request.POST['project_title']
        project_description = request.POST['project_description']
        print("***************************************************", intern_id)
        assign_task = InternProject.objects.create(user_id=intern_id , project_title=project_title, project_description=project_description)
    return render(request, "custom_admin/admin_interns/intern_project.html", context=data)


def internAssignTasks(request):
    # pass the InternProfile names to the template
    # get the data from the template  
    # save the data to the database. 
    
    data={}
    get_intern_profiles = InternProfile.objects.all()
    data['intern'] = get_intern_profiles
    try:
        if(request.method == "POST"):
            intern_id  = request.POST['internname']
            task_title = request.POST['task_title']
            task_description = request.POST['description']
                
            assign_task = InternTasks.objects.create(user_id=intern_id , task_title=task_title, task_description=task_description)
            assigned_intern = InternProfile.objects.get(user_id=intern_id)
            messages.success(request, f"Task assigned to {assigned_intern.user.username}")
    except:
        messages.error(request, "Error Occurred")
    return render(request, "custom_admin/admin_interns/assign_tasks.html", context=data)

def internCheckTask(request):
    data = {}
    
    # Get search query from the request
    search_query = request.GET.get('search', '')
    
    # Filter tasks by search query (student username or task title)
    if search_query:
        tasks = InternTasks.objects.filter(
            Q(user__username__icontains=search_query) | 
            Q(task_title__icontains=search_query)
        )
    else:
        tasks = InternTasks.objects.all()  # If no search, return all tasks
    
    # Add the tasks to the context
    data['tasks'] = tasks    
    return render(request, "custom_admin/admin_interns/check_tasks.html", context=data)

def internCheckProjects(request):
    data = {}
    
    # Get search query from the request
    search_query = request.GET.get('search', '')
    
    # Filter tasks by search query (student username or task title)
    if search_query:
        projects = InternProject.objects.filter(
            Q(user__username__icontains=search_query) | 
            Q(task_title__icontains=search_query)
        )
    else:
        projects = InternProject.objects.all()  # If no search, return all tasks
    
    # Add the tasks to the context
    data['projects'] = projects    
    return render(request, "custom_admin/admin_interns/check_projects.html", context=data)

# employee
def add_employee_profile(request):
    data = {}
    get_users = User.objects.all()
    data['users'] = get_users

    if request.method == "POST":
        username = request.POST['username']
        designation = request.POST['designation']
        monthly_salary = request.POST['monthly_salary']
        annual_salary = request.POST['annual_salary']
        if(EmployeeProfile.objects.filter(user_id=username).exists()):
            messages.error(request, "Employee Profile already exists")
        else:

            save_profile = EmployeeProfile.objects.create(user_id=username, designation=designation, monthly_salary=monthly_salary, total_salary=annual_salary)
            messages.success(request, "Profile created sucessfully.")
    return render(request, "custom_admin/admin_employees/add_profile_employee.html", context=data)

def manage_employee_profile(request):
    data={}
    course = request.GET.get('course')
    get_employee_profiles = EmployeeProfile.objects.all()
    if course:
        get_intern_profiles = EmployeeProfile.objects.filter(internship_name__icontains=course)
    
    else:
        get_employee_profiles = EmployeeProfile.objects.all()
    if request.method == "POST":
        query = request.POST.get('search')

        if query:
           get_employee_profiles = EmployeeProfile.objects.filter(Q(user__username__icontains=query) | Q (user__first_name__icontains=query) | Q(user__last_name__icontains=query))
      
    data['all_profiles'] = get_employee_profiles
    return render(request, "custom_admin/admin_employees/manage_profile_employee.html", context=data)

def view_profile_employee(request, user_id):
    data={}
    get_user = EmployeeProfile.objects.get(user_id = user_id)
    data['employee'] = get_user
    print(get_user.image)
    if not get_user.image:
        get_user.image = f"{settings.STATIC_URL}default_profile.jpg"
    return render(request, "custom_admin/admin_employees/view_profile_employee.html", context=data)

def edit_profile_employee(request, user_id):
    data = {}
    try:
        get_user_profile = EmployeeProfile.objects.get(user_id=user_id)
        get_user = User.objects.get(id=user_id)
        data['employee'] = get_user_profile

        if not get_user_profile.image:
            get_user_profile.image = f"{settings.STATIC_URL}default_profile.jpg"

        if request.method == "POST":
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            phone_number = request.POST['phone_number']
            designation = request.POST['designation']
            education = request.POST['education']

            # Update user fields
            get_user.first_name = first_name
            get_user.last_name = last_name
            get_user.save()

            # Update profile fields
            get_user_profile.phone = phone_number
            get_user_profile.designation = designation
            get_user_profile.education = education
            get_user_profile.save()  # Save profile changes

            messages.success(request, "Data saved successfully.")
    except EmployeeProfile.DoesNotExist:
        messages.error(request, "Employee profile not found.")
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")

    return render(request, "custom_admin/admin_employees/edit_profile_employee.html", context=data)

def salary_details(request):
    data={}
    get_employee = EmployeeProfile.objects.all()
    data['employees'] = get_employee
    total_salary = 0

    for employee in get_employee:
        total_salary += employee.monthly_salary
    data['total_salary'] = total_salary
    return render(request, "custom_admin/admin_employees/salary_details.html", context=data)