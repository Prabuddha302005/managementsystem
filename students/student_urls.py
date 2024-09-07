from django.urls import path
from students import views

urlpatterns = [
    path('profile/', views.studentProfile),
    path('fees/', views.studentfeesDetails),
]