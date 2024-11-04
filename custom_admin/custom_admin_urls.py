from django.urls import path
from custom_admin import views

urlpatterns = [
   path('login/', views.admin_login),
   path('dashboard/', views.dashboard),
   path('add-user/', views.addUser),
   path('add-profile-student/', views.add_student_profile),
   path('students/manage-profiles/', views.manage_student_profile),
   path('students/view/<user_id>', views.view_profile_student),
   path('students/edit/<user_id>', views.edit_profile_student),
   path('students/add-notes/', views.studentAddNotes),
   path('students/assign-task/', views.studentAssignTask),
   path('students/check-task/', views.studentAssignTaskCheck),
   path('students/update-fees/<user_id>', views.update_student_fees),
   path('students/fees-history/<user_id>', views.student_fees_history),

   # interns 
   path('add-profile-intern/', views.add_intern_profile),
   path('interns/manage-profiles/', views.manage_interns_profile),
   path('interns/view/<user_id>', views.view_profile_intern),
   path('interns/edit/<user_id>', views.edit_profile_intern),
   path('interns/update-fees/<user_id>', views.update_intern_fees),
   path('interns/fees-history/<user_id>', views.intern_fees_history),
   path('interns/add-notes/', views.internAddNotes),
   path('interns/assign-project/', views.internAssignProject),
   path('interns/assign-task/', views.internAssignTasks),
   path('interns/check-tasks/', views.internCheckTask),
   path('interns/check-projects/', views.internCheckProjects),

   #employee
   path('add-profile-employee/', views.add_employee_profile),
   path('employee/manage-profile-employee/', views.manage_employee_profile),
   path('employee/view/<user_id>', views.view_profile_employee),
   path('employee/edit/<user_id>', views.edit_profile_employee),
   path('employee/salary-details', views.salary_details),
   # path('employee/add-salary/<user_id>', views.add_salary_employee),
   

]


