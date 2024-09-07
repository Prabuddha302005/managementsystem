from django.contrib import admin
from students.models import StudentProfile, StudentsTasks
from interns.models import InternProfile
from employee.models import EmployeeProfile
# Register your models here.
class StudentProfileAdmin(admin.ModelAdmin):
    search_fields = ['user__username']
    list_display = ('user', 'phone', 'course_name', 'fees_paid', 'fees_pending', 'total_fees')
    fields = ('user', 'course_name', 'remark', 'total_fees', 'fees_paid', 'fees_pending')

admin.site.register(StudentProfile, StudentProfileAdmin)
class InternProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'internship_name', 'fees_paid', 'fees_pending', 'total_fees')
    fields = ('user', 'internship_name', 'remark', 
              'notes', 'videos', 'tasks', 'total_fees', 'fees_paid', 'fees_pending')
admin.site.register(InternProfile, InternProfileAdmin)


class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'designation', 'monthly_salary', 'total_salary')
    fields = ('user', 'designation',
              'monthly_salary', 'total_salary')
admin.site.register(EmployeeProfile, EmployeeProfileAdmin)

class StudentsTasksAdmin(admin.ModelAdmin):
    list_display = ('user', 'task_title', 'task_description', 'assignment')  # Display more relevant fields
    fields = ['user', 'task_title', 'task_description']  # Include task title and assignment field
    search_fields = ['user__username', 'task_title']  # Enable searching by username or task title
    list_filter = ['user']  # Filter tasks by user

admin.site.register(StudentsTasks, StudentsTasksAdmin)

