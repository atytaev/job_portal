from django.db import models
from django.contrib.auth import get_user_model
from jobs.models import Job

User = get_user_model()

class Resume(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='resume')
    name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=20)
    Birth = models.DateField()
    skills = models.TextField()
    GENDER_CHOICES = (
        ('M', 'Мужчина'),
        ('F', 'Женщина'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    city = models.CharField(max_length=255)
    experience = models.TextField()
    education = models.TextField()
    contact_info = models.TextField()
    phone = models.CharField(max_length=13)

    def __str__(self):
        return f"Резюме {self.user.username}"

class JobApplication(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='applications')
    cover_letter = models.TextField()
    is_approved = models.BooleanField(default=False)  # Утверждено ли работодателем
    is_read = models.BooleanField(default=False)  # Прочитан ли отклик работодателем
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Заявка {self.user.username} на вакансию {self.job.title}"


