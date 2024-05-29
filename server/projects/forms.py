from django import forms
from .models import Projects


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Projects
        exclude = ['image', 'created_at', 'owner', 'participants']
