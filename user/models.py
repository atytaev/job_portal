from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('COMPANY', 'Компания'),
        ('APPLICANT', 'Соискатель'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='APPLICANT')
    company_name = models.CharField(
        max_length=255,
        verbose_name="Company name:"
    )
    phone_number = models.CharField(max_length=13, blank=True, null=True)
    def __str__(self):
        return self.username