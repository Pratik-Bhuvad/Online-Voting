from django import forms
from .models import EventRegistration

class EventRegistrationForm(forms.ModelForm):
    college_id = forms.CharField(max_length=50, required=True, label="College ID")
    student_class = forms.CharField(max_length=100, required=True, label="Class")
    division = forms.CharField(max_length=10, required=True, label="Division")
    year = forms.CharField(max_length=50, required=True, label="Year")
    course = forms.CharField(max_length=100, required=True, label="Course")
    department = forms.CharField(max_length=100, required=True, label="Department")

    class Meta:
        model = EventRegistration
        fields = ['college_id', 'student_class', 'division', 'year', 'course', 'department']