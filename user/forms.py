from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    ROLE_CHOICES = (
        ('COMPANY', 'Компания'),
        ('APPLICANT', 'Соискатель'),
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES)
    company_name = forms.CharField(max_length=255, required=False, label="Сompany name:")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", 'role', 'company_name', 'phone_number')

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        company_name = cleaned_data.get('company_name')

        if role == 'COMPANY' and not company_name:
            raise forms.ValidationError("Название компании обязательно для пользователей с ролью 'Компания'.")
        return cleaned_data

