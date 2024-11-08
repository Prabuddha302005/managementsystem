from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
import datetime
# Create your models here.


class InternProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to User
    phone = models.CharField(max_length=50, null=True, blank=True)
    parent_number = models.CharField(max_length=50, null=True, blank=True)
    internship_name = models.CharField(max_length=100, null=True, blank=True)
    education = models.CharField(max_length=100, null=True, blank=True)
    remark = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='intern_images/', null=True, blank=True)
    birth_date = models.DateField(null=True)
    aadhaar_number = models.BigIntegerField(null=True)
    # Fees fields
    total_fees = models.FloatField(null=True, blank=True)
    fees_paid = models.FloatField(null=True, blank=True)
    fees_pending = models.FloatField(null=True, blank=True)

    role = models.CharField(max_length=20, default="Intern")

    def __str__(self):
        return f'{self.user.username} Intern Profile'
    

class InternTasks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Allows multiple tasks for one user
    task_title = models.CharField(max_length=255)  # You can add a task title or identifier
    task_pdf = models.FileField(upload_to='assigned_intern_taks/', max_length=100)
    assignment = models.FileField(upload_to='intern_assignments_tasks/', max_length=100)

    def __str__(self):
        return f"Task for {self.user.username}: {self.task_title}"

class InternNotes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notes_title = models.CharField(max_length=255)
    notes_pdf = models.FileField(upload_to='student_notes/', max_length=100)


    def __str__(self):
        return f"Notes added for {self.user.username}: {self.notes_title}"


class InternProject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project_title = models.CharField(max_length=255)
    project_link = models.URLField(max_length=500, blank=True, null=True)  # Optional field for links (e.g., GitHub)
    project_pdf = models.FileField(upload_to='assigned_intern_projects/', max_length=100)
    project_file = models.FileField(upload_to='intern_projects_submission/', max_length=100, blank=True, null=True)  # Optional field for ZIP file
    submission_date = models.DateTimeField(auto_now_add=True)  # Automatically saves the date of project submission

    def __str__(self):
        return self.project_title
    
class FeesIntern(models.Model):
    time = datetime.datetime.now()
    intern_profile = models.ForeignKey(InternProfile, on_delete=models.CASCADE)  # Link to the StudentProfile
    total_fees = models.DecimalField(max_digits=10, decimal_places=2)  # Total fee amount
    paid_fees = models.DecimalField(max_digits=10, decimal_places=2)   # Amount paid
    pending_fees = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))  # Automatically calculated
    fees_remark = models.TextField(blank=True, null=True)  # Optional remark
    installment_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    date_time = models.DateTimeField(default=time)
    def save(self, *args, **kwargs):
        # Automatically calculate the pending fees before saving
        self.pending_fees = float(self.total_fees) - float(self.paid_fees)
        super().save(*args, **kwargs)  # Call the parent class's save method