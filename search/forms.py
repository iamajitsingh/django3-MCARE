from django import forms
from django.forms import ModelForm
from .models import Post


class SearchForm(forms.Form):
    search = forms.CharField(max_length=30)


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['op', 'patient', 'age', 'gender', 'state', 'district', 'resource', 'contact_email', 'contact_phone']
        labels = {
            'op': 'Posted By',
            'patient': 'Name of Patient',
            'age': 'Patient Category',
            'gender': 'Gender of Patient',
            'resource': 'Resource required',
            'contact_email': 'Your contact e-mail',
            'contact_phone': 'Your contact number'
        }
