from django import forms
from .models import Post
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget



class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'image', 'category', 'text' ]
        widgets = {
            'text': SummernoteWidget(),
        }


class ContactForm(forms.Form):
    name = forms.CharField(max_length=255)
    text = forms.CharField(max_length=20)
    email = forms.EmailField()
    message = forms.CharField(max_length=1000)