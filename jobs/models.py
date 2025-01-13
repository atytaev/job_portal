from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class Job(models.Model):
    CURRENCY_CHOICES = [
        ('USD', 'USD'),
        ('EUR', 'EUR'),
        ('RUB', 'RUB'),
        ('GBP', 'GBP'),
        ('BYN', 'BYN'),

    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    currency = models.CharField(choices=CURRENCY_CHOICES, max_length=3, default='BYN')
    created_at = models.DateTimeField(auto_now_add=True)
    company = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jobs', null=True)


    def __str__(self):
        return self.title