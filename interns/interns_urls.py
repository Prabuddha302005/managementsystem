from django.urls import path
from interns import views

urlpatterns = [
   path('intern/', views.InternHome),
]
