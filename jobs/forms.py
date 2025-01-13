from django import forms
from .models import Job


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'location', 'salary']


class JobFilterForm(forms.Form):
    job_type_choices = (
        ('full_time', 'Полная занятость'),
        ('part_time', 'Частичная занятость'),
        ('freelance', 'Удаленная работа'),
    )
    title = forms.CharField(required=False, label='Название вакансии', widget=forms.TextInput(attrs={'placeholder': 'Поиск по названию'}))
    company = forms.CharField(required=False, label='Компания', widget=forms.TextInput(attrs={'placeholder': 'Поиск по компании'}))
    location = forms.CharField(required=False, label='Локация', widget=forms.TextInput(attrs={'placeholder': 'Поиск по локации'}))