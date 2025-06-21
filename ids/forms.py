from django import forms
from .models import Student, LossReport


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'course', 'year_of_study', 'mobile', 'student_id']


class ReportLostIDForm(forms.ModelForm):
    class Meta:
        model = LossReport
        fields = ['student_id', 'report_file']
        widgets = {
            'student_id': forms.TextInput(attrs={'placeholder': 'Enter your Student ID'}),
            'report_file': forms.FileInput(attrs={'accept': 'application/pdf,image/*'}),
        }


class FetchStudentForm(forms.Form):
    student_id = forms.CharField(max_length=20, label="Student ID")
