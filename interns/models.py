from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class InternProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to User
    phone = models.CharField(max_length=50, null=True, blank=True)
    parent_number = models.CharField(max_length=50, null=True, blank=True)
    internship_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    education = models.CharField(max_length=100, null=True, blank=True)
    remark = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='intern_images/', null=True, blank=True)

    # Fees fields
    total_fees = models.FloatField(null=True, blank=True)
    fees_paid = models.FloatField(null=True, blank=True)
    fees_pending = models.FloatField(null=True, blank=True)

    # Files
    notes = models.FileField(upload_to='intern_notes/', null=True, blank=True)
    videos = models.FileField(upload_to='intern_videos/', null=True, blank=True)
    tasks = models.FileField(upload_to='intern_tasks/', null=True, blank=True)
    
    # Project fields (for links or zip files)
    project_link = models.URLField(null=True, blank=True)
    project_zip = models.FileField(upload_to='intern_projects/', null=True, blank=True)
    role = models.CharField(max_length=20, default="Intern")

    def __str__(self):
        return f'{self.user.username} Intern Profile'