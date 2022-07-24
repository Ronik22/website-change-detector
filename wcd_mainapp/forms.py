from django import forms
from django.forms.widgets import CheckboxInput
from .models import Tasks

class TasksCreateForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = "__all__"
        exclude = ('user',)

class TasksUpdateForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = "__all__"
        exclude = ('user',)
