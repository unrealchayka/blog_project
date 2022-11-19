from django import forms
from .models import Post, Task
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget



class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'image', 'category', 'text' ]
        widgets = {
            'text': SummernoteWidget(),
        }

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'description')


class ContactForm(forms.Form):
    name = forms.CharField(max_length=255)
    text = forms.CharField(max_length=20)
    email = forms.EmailField()
    message = forms.CharField(max_length=1000)