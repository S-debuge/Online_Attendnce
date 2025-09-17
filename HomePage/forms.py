from django import forms
from .models import Student, Teacher, Parent

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = "__all__"

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = "__all__"

class ParentForm(forms.ModelForm):
    class Meta:
        model = Parent
        fields = "__all__"
