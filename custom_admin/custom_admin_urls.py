from django.urls import path
from custom_admin import views

urlpatterns = [
   path('login/', views.admin_login),
   path('dashboard/', views.dashboard),
   path('students/manage-profiles/', views.manage_student_profile),
   path('students/add-notes', views.studentAddNotes),
   path('students/assign-task', views.studentAssignTask),
]
