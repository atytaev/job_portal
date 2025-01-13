from django.contrib import admin
from .models import Job
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'location', 'salary', 'currency', 'created_at', 'user')
    list_filter = ('currency', 'location', 'company')
    search_fields = ('title', 'description', 'location', 'company')
    autocomplete_fields = ('user',)
    date_hierarchy = 'created_at'
