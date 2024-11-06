from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

import datetime
# Create your models here.
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=50, null=True, blank=True)
    parent_number = models.CharField(max_length=50, null=True, blank=True)
    course_name = models.CharField(max_length=50, null=True, blank=True)
    education = models.CharField(max_length=50, null=True, blank=True)
    remark = models.CharField(max_length=50, null=True, blank=True)
    image = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    birth_date = models.DateField(null=True)
    aadhaar_number = models.BigIntegerField(null=True)
    role = models.CharField(max_length=20, default="Student")

    def __str__(self):
        return f'{self.user.username} Student Profile'
    
class StudentsTasks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    task_title = models.CharField(max_length=255)
    task_pdf = models.FileField(upload_to='student_taks/', max_length=100)
    assignment = models.FileField(upload_to='student_assignments/', max_length=100)

    def __str__(self):
        return f"Task for {self.user.username}: {self.task_title}"

class StudentsNotes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notes_title = models.CharField(max_length=255)
    notes_pdf = models.FileField(upload_to='student_notes/', max_length=100)
    

class Fees(models.Model):
    date = datetime.datetime.now()
    student_profile = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)  # Link to the StudentProfile
    total_fees = models.DecimalField(max_digits=10, decimal_places=2)  # Total fee amount
    paid_fees = models.DecimalField(max_digits=10, decimal_places=2)   # Amount paid
    pending_fees = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))  # Automatically calculated
    fees_remark = models.TextField(blank=True, null=True) 
    installment_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    date_time = models.DateTimeField(default=date)  

    def save(self, *args, **kwargs):
        # Automatically calculate the pending fees before saving
        self.pending_fees = float(self.total_fees) - float(self.paid_fees)
        super().save(*args, **kwargs)  # Call the parent class's save method