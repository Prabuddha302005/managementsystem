from django.urls import path
from students import views

urlpatterns = [
    path('profile/', views.studentProfile),
    path('account/', views.studentfeesDetails),
    path('tasks/', views.StudentTasks),
    path('notes/', views.StudentNotes),
]