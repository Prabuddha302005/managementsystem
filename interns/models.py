from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class InternProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to User
    phone = models.CharField(max_length=50, null=True, blank=True)
    parent_number = models.CharField(max_length=50, null=True, blank=True)
    internship_name = models.CharField(max_length=100, null=True, blank=True)
    education = models.CharField(max_length=100, null=True, blank=True)
    remark = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='intern_images/', null=True, blank=True)

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
    task_description = models.TextField()
    assignment = models.FileField(upload_to='intern_assignments/', max_length=100)

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
    project_description = models.TextField(blank=True, null=True)
    project_link = models.URLField(max_length=500, blank=True, null=True)  # Optional field for links (e.g., GitHub)
    project_file = models.FileField(upload_to='intern_projects/', max_length=100, blank=True, null=True)  # Optional field for ZIP file
    submission_date = models.DateTimeField(auto_now_add=True)  # Automatically saves the date of project submission

    def __str__(self):
        return self.project_title