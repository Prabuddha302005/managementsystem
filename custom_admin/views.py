from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from students.models import StudentsNotes, StudentsTasks, StudentProfile, Fees
from interns.models import InternProfile, InternNotes, InternProject, FeesIntern, InternTasks
from employee.models import EmployeeProfile
from django.contrib import messages
from django.db.models import Q
from django.conf import settings
from django.core.mail import send_mail
from datetime import datetime
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
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
    if request.user.is_authenticated:
        data = {}
        if(request.method == "POST"):
            username = request.POST['username']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            
            
            if(username =="" or first_name == "" or last_name=="" or email == "" or password1 == "" or password2 == "" ):
                messages.error(request, "All fileds are necessary")
            elif(password1 != password2):
                messages.error(request, "Password doesn't match")
            elif(User.objects.filter(username=username).exists()):
                messages.error(request, "Username already exists")
            else:
                user = User.objects.create(username=username, email=email, first_name=first_name, last_name=last_name)
                user.set_password(password1)
                user.save()
                messages.success(request, "User Created successfully")
    else:
        return redirect('/custom-admin/login')
    return render(request, "custom_admin/add_user.html", context=data)


def add_student_profile(request):
    if request.user.is_authenticated:
        data = {}
        get_users = User.objects.all()
        data['users'] = get_users

        if request.method == "POST":
            username = request.POST['username']
            course_name = request.POST['course_name']
            birth_date = request.POST['birth_date']
            aadhaar_number = request.POST['addhar_number']
            student_number = request.POST['student_number']
            parent_number = request.POST['parent_number']
            education = request.POST['education']
            image = request.FILES['image']
            remark = request.POST['remark']
            total_fees = request.POST['total_fees']
            paid_fees = request.POST['paid_fees']
            pending_fees = request.POST['pending_fees']
            fees_remark = request.POST['fees_remark']
            if(StudentProfile.objects.filter(user_id=username).exists()):
                messages.error(request, "Student Profile already exists")
            else:
                save_profile = StudentProfile.objects.create(user_id=username, course_name=course_name, remark=remark, birth_date=birth_date, aadhaar_number=aadhaar_number, phone=student_number, parent_number=parent_number, education=education, image=image)

                Fees.objects.create(
                    student_profile=save_profile, 
                    total_fees=total_fees,
                    paid_fees=paid_fees,
                    pending_fees=pending_fees,  
                    fees_remark=fees_remark,
                    installment_amount = paid_fees
                )
                messages.success(request, "Student Profile created sucessfully.")
    else:
        return redirect('/custom-admin/login')
    return render(request, "custom_admin/admin_students/add_profile_student.html", context=data)

def manage_student_profile(request):
    if request.user.is_authenticated:
        data = {}
        course = request.GET.get('course')
        
        # Get all student profiles based on search or course filter
        get_student_profiles = StudentProfile.objects.all()
        if course:
            get_student_profiles = StudentProfile.objects.filter(course_name__icontains=course)
        if request.method == "POST":
            query = request.POST.get('search')
            if query:
                get_student_profiles = StudentProfile.objects.filter(
                    Q(user__username__icontains=query) |
                    Q(user__first_name__icontains=query) |
                    Q(user__last_name__icontains=query)
                )
        
        # Adding fees details to each profile
        profiles_with_fees = []
        for profile in get_student_profiles:
            # Assuming the `Fees` model has a foreign key to `StudentProfile` named `student_profile`
            fees = Fees.objects.filter(student_profile=profile).last()
            profiles_with_fees.append({
                'profile': profile,
                'paid_fees': fees.paid_fees if fees else 0,
                'pending_fees': fees.pending_fees if fees else 0,
                'total_fees': fees.total_fees if fees else 0,
            })
        
        data['all_profiles'] = profiles_with_fees
    else:
        return redirect('/custom-admin/login')
    return render(request, "custom_admin/admin_students/manage_profile.html", context=data)

@login_required(login_url='/custom-admin/login')
def studentAddNotes(request):
    if request.user.is_authenticated:
        data = {}
        try:
            # Retrieve all student profiles
            getStudents = StudentProfile.objects.all()
            data['students'] = getStudents
            
            if request.method == "POST":
                # Retrieve data from the form
                student_id = request.POST['studentname']
                notestitle = request.POST['notestitle']
                notesfile = request.FILES.get('notesfile')
                
                # Debug print statement
                print("=======>", student_id, notestitle, notesfile)
                
                # Save notes to the database
                assign_notes = StudentsNotes.objects.create(user_id=student_id, notes_title=notestitle, notes_pdf=notesfile)
                
                # Retrieve the student's email from the profile
                student_profile = User.objects.get(id=student_id)
                student_email = student_profile.email  # Assumes there's a related `User` model with an `email` field
                
                # Prepare and send the email
                subject = 'New Notes Added to Your Profile'
                message = f'''Hello {student_profile.username},

    New notes titled "{notestitle}" have been added to your profile by the admin. 

    You can now access these notes in your account.

    Best regards,
    The Team
                '''
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [student_email]
                
                send_mail(subject, message, email_from, recipient_list)

                # Display a success message
                messages.success(request, "Notes added successfully, and the student has been notified via email.")
        except Exception as e:
            # Display an error message if something goes wrong
            messages.error(request, f"Some error occurred: {str(e)}")
    else:
        return redirect('/custom-admin/login')
            
    return render(request, "custom_admin/admin_students/addNotes.html", context=data)


@login_required(login_url='/custom-admin/login')
def studentAssignTask(request):
    
    data = {}
    try:
        getStudents = StudentProfile.objects.all()
        data['students'] = getStudents
        if(request.method == "POST"):
            student_id  = request.POST['studentname']
            task_title = request.POST['task_title']
            taskfile = request.FILES.get('taskfile')
            
            assign_task = StudentsTasks.objects.create(user_id=student_id , task_title=task_title, task_pdf=taskfile)
            # Retrieve the student's email from the profile
            student_profile = User.objects.get(id=student_id)
            student_email = student_profile.email  # Assumes there's a related `User` model with an `email` field
            
            # Prepare and send the email
            subject = 'New Notes Added to Your Profile'
            message = f'''Hello {student_profile.username},

New Task titled "{task_title}" have been assigned to you by the admin. 

You can now check the task in your account.

Best regards,
The Team
            '''
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [student_email]
            
            send_mail(subject, message, email_from, recipient_list)
            messages.success(request, f"Task assigned successfully")
    except Exception as e:
        messages.error(request, f"Some error occurred {str(e)}")
    return render(request, "custom_admin/admin_students/assign_task.html", context=data)

@login_required(login_url='/custom-admin/login')
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

@login_required(login_url='/custom-admin/login')
def deleteStudentTasks(request, id):
    try:
        get_task = get_object_or_404(StudentsTasks, id=id)
        get_task.delete()
        messages.success(request, "Task deleted successfully")
        return redirect("/custom-admin/students/check-task/")
    except:
        messages.error(request, "Some error occurred")
        return redirect("/custom-admin/students/check-task/")



@login_required(login_url='/custom-admin/login')
def view_profile_student(request, user_id):
    data={}
    user = get_object_or_404(User, id=user_id)
    get_user = StudentProfile.objects.get(user_id = user_id)
    get_fees = Fees.objects.get(student_profile__user=user)
    data['student'] = get_user
    data['total_fees'] = get_fees
    if not get_user.image:
        get_user.image = f"{settings.STATIC_URL}default_profile.jpg"
    return render(request, "custom_admin/admin_students/view_profile.html", context=data)

@login_required(login_url='/custom-admin/login')
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

@login_required(login_url='/custom-admin/login')
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
            fees_remark=fees_remark,
            installment_amount=paid_fees
        )

        # Display a success message
        messages.success(request, "Payment successfully added and fees updated.")
      # Redirect to the fees list or appropriate page

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

@login_required(login_url='/custom-admin/login')
def delete_student_profile(request, user_id):
    try:
        # Get and delete the user from auth_user
        student_user = get_object_or_404(User, id=user_id)
        student_profile = get_object_or_404(StudentProfile, user_id=user_id)  # Assuming user_id is the foreign key

        # Delete both the user and profile
        student_user.delete()
        student_profile.delete()
        
        messages.success(request, f"Student {student_user.username} deleted successfully.")
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
    return redirect("/custom-admin/students/manage-profiles/")


# interns
@login_required(login_url='/custom-admin/login')
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
        birth_date = request.POST['birth_date']
        aadhaar_number = request.POST['addhar_number']
        phone = request.POST['intern_number']
        parent_number = request.POST['parent_number']
        education = request.POST['education']
        image = request.FILES['image']
        if(InternProfile.objects.filter(user_id=username).exists()):
            messages.error(request, "Intern Profile already exists")
        else:

            save_profile = InternProfile.objects.create(user_id=username, internship_name=internship_name, remark=remark, birth_date=birth_date, phone=phone, aadhaar_number=aadhaar_number, parent_number=parent_number, education=education, image=image)

            FeesIntern.objects.create(
                intern_profile=save_profile,  # Link to the intern profile instance
                total_fees=total_fees,
                paid_fees=paid_fees,
                pending_fees=pending_fees,  # Automatically calculated
                fees_remark=fees_remark,
                installment_amount=paid_fees
            
            )
            messages.success(request, "Profile created sucessfully.")
    return render(request, "custom_admin/admin_interns/add_profile_intern.html", context=data)

@login_required(login_url='/custom-admin/login')
def manage_interns_profile(request):
    data = {}
    course = request.GET.get('course')
    
    # Fetch all intern profiles based on filters
    get_intern_profiles = InternProfile.objects.all()
    if course:
        get_intern_profiles = get_intern_profiles.filter(internship_name__icontains=course)
    if request.method == "POST":
        query = request.POST.get('search')
        if query:
            get_intern_profiles = get_intern_profiles.filter(
                Q(user__username__icontains=query) |
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query)
            )

    # Adding fees details to each intern profile
    profiles_with_fees = []
    for profile in get_intern_profiles:
        # Fetch the last fees record for each intern profile
        fees = FeesIntern.objects.filter(intern_profile=profile).last()
        profiles_with_fees.append({
            'profile': profile,
            'paid_fees': fees.paid_fees if fees else 0,
            'pending_fees': fees.pending_fees if fees else 0,
            'total_fees': fees.total_fees if fees else 0,
        })

    data['all_profiles'] = profiles_with_fees
    return render(request, "custom_admin/admin_interns/manage_profile.html", context=data)

@login_required(login_url='/custom-admin/login')
def view_profile_intern(request, user_id):
    data={}
    get_user = InternProfile.objects.get(user_id = user_id)
    data['intern'] = get_user
    if not get_user.image:
        get_user.image = f"{settings.STATIC_URL}default_profile.jpg"
    
    return render(request, "custom_admin/admin_interns/view_profile.html", context=data)


@login_required(login_url='/custom-admin/login')
def edit_profile_intern(request, user_id):
    data={}
    try:
        get_user_profile = InternProfile.objects.get(user_id = user_id)
        get_user = User.objects.get(id=user_id)
        data['intern'] = get_user_profile
        if not get_user_profile.image:
           get_user_profile.image = f"{settings.STATIC_URL}default_profile.jpg"


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

@login_required(login_url='/custom-admin/login')
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
            fees_remark=fees_remark,
            installment_amount=paid_fees
        )

        # Display a success message
        messages.success(request, "Payment successfully added and fees updated.")

    # Pass data to the template for display
    data = {
        'user': user,
        'last_total_fees': last_fee_record.total_fees if last_fee_record else '',
        'last_pending_fees': last_fee_record.pending_fees if last_fee_record else '',
        
    }
    return render(request, "custom_admin/admin_interns/update_fees.html", context=data)

@login_required(login_url='/custom-admin/login')
def delete_intern_profile(request, user_id):
    try:
        # Get and delete the user from auth_user
        intern_user = get_object_or_404(User, id=user_id)
        intern_profile = get_object_or_404(InternProfile, user_id=user_id)  # Assuming user_id is the foreign key

        # Delete both the user and profile
        intern_user.delete()
        intern_profile.delete()
        
        messages.success(request, f"Intern {intern_user.username} deleted successfully.")
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
    return redirect("/custom-admin/interns/manage-profiles/")

@login_required(login_url='/custom-admin/login')
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

@login_required(login_url='/custom-admin/login')
def internAddNotes(request):
    data = {}
    try:

        getIntern = InternProfile.objects.all()
        data['interns'] = getIntern
        if(request.method == "POST"):
            intern_id  = request.POST['intername']
            notestitle = request.POST['notestitle']
            notesfile = request.FILES.get('notesfile')
            print("=======>", intern_id , notestitle, notesfile)
                
            assign_notes = InternNotes.objects.create(user_id=intern_id , notes_title=notestitle, notes_pdf=notesfile)

            messages.success(request, "Notes added to the intern")
    except Exception as e:
        messages.error(request, f"Some error occurred {str(e)}")
    return render(request, "custom_admin/admin_interns/add_notes.html", context=data)

@login_required(login_url='/custom-admin/login')
def internAssignProject(request):
    data = {}
    try:
        getInterns = InternProfile.objects.all()
        data['interns'] = getInterns
        if(request.method == "POST"):
            intern_id  = request.POST['internname']
            project_title = request.POST['project_title']
            project_pdf = request.FILES.get('project_pdf')
            print("***************************************************", intern_id)
            assign_project = InternProject.objects.create(user_id=intern_id , project_title=project_title, project_pdf=project_pdf)
            messages.success(request, "Project assigned to the Intern")
    except Exception as e:
        messages.error(request, f"Some error occurred {str(e)}")
    return render(request, "custom_admin/admin_interns/intern_project.html", context=data)

@login_required(login_url='/custom-admin/login')
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
            task_pdf = request.FILES.get('task_pdf')
        
                
            assign_task = InternTasks.objects.create(user_id=intern_id , task_title=task_title, task_pdf=task_pdf)
            assigned_intern = InternProfile.objects.get(user_id=intern_id)
            messages.success(request, f"Task assigned to {assigned_intern.user.username}")
    except Exception as e:
        messages.error(request, f"Error Occurred {str(e)}")
    return render(request, "custom_admin/admin_interns/assign_tasks.html", context=data)

@login_required(login_url='/custom-admin/login')
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

@login_required(login_url='/custom-admin/login')
def deleteTaskIntern(request, id):
    try:

        get_task = get_object_or_404(InternTasks, id=id)
        get_task.delete()
        messages.success(request, "Task deleted successfully")
        return redirect("/custom-admin/interns/check-tasks/")
       
    except:
        messages.error(request, "Some error occurred")
        return redirect("/custom-admin/interns/check-tasks/")
     

@login_required(login_url='/custom-admin/login')
def internCheckProjects(request):
    data = {}
    
    # Get search query from the request
    search_query = request.GET.get('search', '')
    
    # Filter tasks by search query (student username or task title)
    if search_query:
        projects = InternProject.objects.filter(
            Q(user__username__icontains=search_query) | 
            Q(project_title__icontains=search_query)
        )
    else:
        projects = InternProject.objects.all()  # If no search, return all tasks
    
    # Add the tasks to the context
    data['projects'] = projects    
    return render(request, "custom_admin/admin_interns/check_projects.html", context=data)

@login_required(login_url='/custom-admin/login')
def deleteProjectIntern(request, id):
    try:

        get_project = get_object_or_404(InternProject, id=id)
        get_project.delete()
        messages.success(request, "Project deleted successfully")
        return redirect("/custom-admin/interns/check-projects/")
       
    except:
        messages.error(request, "Some error occurred")
        return redirect("/custom-admin/interns/check-projects/")
    

# employee
@login_required(login_url='/custom-admin/login')
def add_employee_profile(request):
    data = {}
    get_users = User.objects.all()
    data['users'] = get_users

    if request.method == "POST":
        username = request.POST['username']
        designation = request.POST['designation']
        monthly_salary = request.POST['monthly_salary']
        annual_salary = request.POST['annual_salary']
        birth_date = request.POST['birth_date']
        addhar_number = request.POST['addhar_number']
        employee_number = request.POST['employee_number']
        image = request.FILES.get('image')
        
        if(EmployeeProfile.objects.filter(user_id=username).exists()):
            messages.error(request, "Employee Profile already exists")
        else:

            save_profile = EmployeeProfile.objects.create(user_id=username, designation=designation, monthly_salary=monthly_salary, total_salary=annual_salary, birth_date=birth_date, aadhaar_number=addhar_number, phone=employee_number, image=image)
            messages.success(request, "Profile created sucessfully.")
    return render(request, "custom_admin/admin_employees/add_profile_employee.html", context=data)

@login_required(login_url='/custom-admin/login')
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

@login_required(login_url='/custom-admin/login')
def view_profile_employee(request, user_id):
    data={}
    get_user = EmployeeProfile.objects.get(user_id = user_id)
    data['employee'] = get_user
    print(get_user.image)
    if not get_user.image:
        get_user.image = f"{settings.STATIC_URL}default_profile.jpg"
    return render(request, "custom_admin/admin_employees/view_profile_employee.html", context=data)

@login_required(login_url='/custom-admin/login')
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

@login_required(login_url='/custom-admin/login')
def salary_details(request):
    data = {}
    get_employee = EmployeeProfile.objects.all()

    # Monthly salary total (assuming current month)
    current_month = datetime.now().month
    current_year = datetime.now().year
    monthly_total_salary = get_employee.aggregate(
        monthly_total=Sum('monthly_salary')
    )['monthly_total'] or 0  # Set to 0 if no employees

    # Yearly salary total
    yearly_total_salary = monthly_total_salary * 12

    # Adding annual salary for each employee
    for employee in get_employee:
        employee.annual_salary = employee.monthly_salary * 12

    # Passing data to the template
    data['employees'] = get_employee
    data['monthly_total_salary'] = monthly_total_salary
    data['yearly_total_salary'] = yearly_total_salary
    data['current_month'] = datetime.now().strftime("%B")
    data['current_year'] = current_year
    
    return render(request, "custom_admin/admin_employees/salary_details.html", context=data)
    
@login_required(login_url='/custom-admin/login')
def delete_employee(request, user_id):
    try:
        # Get and delete the user from auth_user
        employee_user = get_object_or_404(User, id=user_id)
        employee_profile = get_object_or_404(EmployeeProfile, user_id=user_id)  # Assuming user_id is the foreign key

        # Delete both the user and profile
        employee_user.delete()
        employee_profile.delete()
        
        messages.success(request, f"Employee {employee_user.username} deleted successfully.")
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
    return redirect("/custom-admin/employee/manage-profile-employee/")