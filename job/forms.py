from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from .models import Application, Job


class SignupForm(UserCreationForm):
    """Professional registration form with standardized Bootstrap styling."""
    
    # Adding help_text to the email field improves UX
    email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'name@company.com'})
    )

    class Meta:
        model = User
        fields = ["username", "email"]
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Choose a unique username'
            }),
        }
        help_texts = {
            'username': 'This will be your public display name.',
        }
from django import forms
from .models import Job

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ["title", "description", "company", "location", "salary"]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control form-control-lg', 
                'placeholder': 'e.g. Senior Backend Engineer'
            }),
            'company': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Company Name'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'e.g. Remote or New York, NY'
            }),
            'salary': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'e.g. 100000'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 6, 
                'placeholder': 'What are the main responsibilities?'
            }),
        }
        help_texts = {
            'salary': 'Annual base salary in USD.',
            'description': 'Clearly define the role requirements and benefits.',
        }

    def clean_salary(self):
        salary = self.cleaned_data.get('salary')
        if salary and salary < 0:
            raise forms.ValidationError("Salary cannot be negative.")
        return salary



class ApplicationForm(forms.ModelForm):
    """Secure application form with file validation and improved UX attributes."""
    class Meta:
        model = Application
        fields = ["cv", "cover_letter"]
        widgets = {
            'cv': forms.FileInput(attrs={
                'class': 'form-control', 
                'accept': '.pdf,.docx' # Improves browser file picker UX
            }),
            'cover_letter': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 5, 
                'placeholder': 'Explain why you are the perfect fit for this role...'
            }),
        }
        help_texts = {
            'cv': 'Please upload your CV in PDF or DOCX format.',
            'cover_letter': 'A compelling cover letter increases your chances of an interview.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Enforce file constraints at the form level
        self.fields['cv'].validators.append(
            FileExtensionValidator(
                allowed_extensions=['pdf', 'docx'], 
                message="Only PDF or DOCX files are accepted."
            )
        )