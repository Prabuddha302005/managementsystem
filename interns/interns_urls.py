from django.urls import path
from interns import views

urlpatterns = [
   path('profile/', views.internProfile),
   path('notes/', views.internNote),
   path('tasks/', views.internTask),
   path('projects/', views.internProject),
   path('account/', views.internFees),
]
