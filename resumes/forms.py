from django import forms
from .models import Resume, JobApplication

class ResumeForm(forms.ModelForm):
    Birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True,
        label="Дата рождения"
    )

    def clean_birth_date(self):
        Birth = self.cleaned_data['birth_date']
        if Birth > date.today():
            raise forms.ValidationError("Дата рождения не может быть в будущем!")
        return Birth
    class Meta:
        model = Resume
        fields = ['first_name', 'last_name', 'Birth', 'skills', 'gender', 'city', 'experience', 'education',
                  'contact_info', 'phone']


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['cover_letter']