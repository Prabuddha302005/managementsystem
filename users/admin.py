# from django.contrib import admin
# from students.models import StudentProfile, StudentsTasks, StudentsNotes
# from interns.models import InternProfile, InternNotes, InternProject, InternTasks
# from employee.models import EmployeeProfile
# from django.utils.html import format_html

# # Register your models here.

# # Student related models 
# class StudentProfileAdmin(admin.ModelAdmin):
#     search_fields = ['user__username']
#     list_display = ('user', 'phone', 'course_name')
#     fields = ('user', 'course_name', 'remark')

# admin.site.register(StudentProfile, StudentProfileAdmin)

# class StudentsTasksAdmin(admin.ModelAdmin):
#     list_display = ('user', 'task_title', 'task_description', 'assignment')  # Display more relevant fields
#     fields = ['user', 'task_title', 'task_description']  # Include task title and assignment field
#     search_fields = ['user__username', 'task_title']  # Enable searching by username or task title
#     list_filter = ['user']  # Filter tasks by user

#     def assignment_link(self, obj):
#         if obj.assignment:
#             return format_html('<a href="{}" target="_blank">View Assignment</a>', obj.assignment.url)
#         return "No Assignment Uploaded"
    
#     assignment_link.short_description = "Assignment"

# admin.site.register(StudentsTasks, StudentsTasksAdmin)

# class StudentsNotesAdmin(admin.ModelAdmin):
#    list_display = ('user', 'notes_title', 'notes_pdf') 
#    fields = ('user', 'notes_title', 'notes_pdf')
#    search_fields = ['user__username', 'notes_title']
# admin.site.register(StudentsNotes, StudentsNotesAdmin)

# # Intern related models
# class InternProfileAdmin(admin.ModelAdmin):
#     list_display = ('user', 'internship_name', 'fees_paid', 'fees_pending', 'total_fees')
#     fields = ('user', 'internship_name', 'remark', 
#               'notes', 'videos', 'tasks', 'total_fees', 'fees_paid', 'fees_pending')
# admin.site.register(InternProfile, InternProfileAdmin)

# class InternNotesAdmin(admin.ModelAdmin):
#    list_display = ('user', 'notes_title', 'notes_pdf') 
#    fields = ('user', 'notes_title', 'notes_pdf')
#    search_fields = ['user__username', 'notes_title']   
# admin.site.register(InternNotes, InternNotesAdmin)

# class InternTasksAdmin(admin.ModelAdmin):
#    list_display = ('user', 'task_title', 'task_description', 'assignment') 
#    fields = ('user', 'task_title', 'task_description')
#    search_fields = ['user__username', 'task_title']  

# admin.site.register(InternTasks, InternTasksAdmin)

# class InternProjectAdmin(admin.ModelAdmin):
#     list_display = ('user', 'project_title', 'submission_date', 'project_link', 'project_file')  # Displays these fields in the list view
#     search_fields = ('project_title', 'user__username')  # Enables search functionality by project title and username
#     list_filter = ('submission_date',)  # Adds a filter by submission date
#     fields = ('user', 'project_title', 'project_description')  # Fields to show in the form
# admin.site.register(InternProject, InternProjectAdmin)


# # Employee related models
# class EmployeeProfileAdmin(admin.ModelAdmin):
#     list_display = ('user', 'designation', 'monthly_salary', 'total_salary')
#     fields = ('user', 'designation',
#               'monthly_salary', 'total_salary')
# admin.site.register(EmployeeProfile, EmployeeProfileAdmin)

