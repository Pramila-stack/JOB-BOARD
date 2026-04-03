from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    ROLE_CHOICES = (
        ("seeker","Seeker"),
        ("employer","Employer"),
    )
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    role = models.CharField(max_length=20,choices=ROLE_CHOICES)
    image = models.ImageField(upload_to="images/",blank=False)


    def __str__(self):
        return f"{self.user.username} - {self.role}"
    
class Job(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    company = models.CharField(max_length=200)
    location = models.TextField()
    salary = models.PositiveBigIntegerField()
    posted_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name="jobs")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.company}"
    
class Application(models.Model):
    STATUS_CHOICES = (
        ("pending","Pending"),
        ("confirmed","Confirmed"),
        ("cancelled","Cancelled"),
    )

    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="application_users")
    job = models.ForeignKey(Job,on_delete=models.CASCADE,related_name="application_jobs")
    cv = models.FileField(upload_to="cv/")
    cover_letter = models.TextField()
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default="pending")
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user","job")

    def __str__(self):
        return f"{self.user.username} - {self.job.title}"