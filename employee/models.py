from django.db import models
from django.contrib.auth.models import User

class EmployeeProfile(models.Model):
    # Link to the User model
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Personal Information
    phone = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    designation = models.CharField(max_length=100, null=True, blank=True)
    education = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='employee_images/', null=True, blank=True)

    # Salary Information
    monthly_salary = models.FloatField(null=True, blank=True)
    total_salary = models.FloatField(null=True, blank=True)
    role = models.CharField(max_length=20, default="Employee")

    def __str__(self):
        return f'{self.user.username} Employee Profile'
