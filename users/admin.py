from django.contrib import admin
from students.models import StudentProfile, StudentsTasks, StudentsNotes
from interns.models import InternProfile
from employee.models import EmployeeProfile
from django.utils.html import format_html
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

    def assignment_link(self, obj):
        if obj.assignment:
            return format_html('<a href="{}" target="_blank">View Assignment</a>', obj.assignment.url)
        return "No Assignment Uploaded"
    
    assignment_link.short_description = "Assignment"

admin.site.register(StudentsTasks, StudentsTasksAdmin)


class StudentsNotesAdmin(admin.ModelAdmin):
   list_display = ('user', 'notes_title', 'notes_pdf') 
   fields = ('user', 'notes_title', 'notes_pdf')
   search_fields = ['user__username', 'notes_title']
admin.site.register(StudentsNotes, StudentsNotesAdmin)