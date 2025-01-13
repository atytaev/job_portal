from django.contrib import admin
from .models import Resume, JobApplication
@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'first_name', 'last_name', 'city', 'phone', 'gender')
    list_filter = ('gender', 'city')
    search_fields = ('name', 'first_name', 'last_name', 'city', 'skills')
    autocomplete_fields = ('user',)

# Настройка панели для модели JobApplication
@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'user', 'resume', 'is_approved', 'is_read', 'created_at')
    list_filter = ('is_approved', 'is_read', 'job__title', 'job__company')
    search_fields = ('job__title', 'job__company', 'user__username', 'resume__name')
    autocomplete_fields = ('job', 'user', 'resume')
    date_hierarchy = 'created_at'
