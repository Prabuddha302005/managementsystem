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
]
