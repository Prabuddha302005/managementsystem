from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=50, null=True, blank=True)
    parent_number = models.CharField(max_length=50, null=True, blank=True)
    course_name = models.CharField(max_length=50, null=True, blank=True)
    education = models.CharField(max_length=50, null=True, blank=True)
    remark = models.CharField(max_length=50, null=True, blank=True)
    image = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    total_fees = models.FloatField(null=True, blank=True)
    fees_paid = models.FloatField(null=True, blank=True)
    fees_pending = models.FloatField(null=True, blank=True)  # Corrected the typo
    assignments = models.FileField(upload_to='student_assignments/', blank=True, null=True)
    role = models.CharField(max_length=20, default="Student")

    def __str__(self):
        return f'{self.user.username} Student Profile'