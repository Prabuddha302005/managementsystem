from django.urls import path
from students import views

urlpatterns = [
    path('home/', views.StudentHome),
    path('profile/', views.studentProfile),
    path('fees/', views.studentfeesDetails),
]
