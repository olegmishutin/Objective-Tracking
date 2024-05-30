from django import forms
from .models import Projects, Task


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Projects
        exclude = ['image', 'created_at', 'owner', 'participants']


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ['created_at', 'executor', 'project']
