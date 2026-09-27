from typing import Any

from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView

from blog.models import Message, article


class ContactUsForm(forms.Form):
    name = forms.CharField(label='Name', max_length=10)
    email = forms.EmailField(label='Email')
    subject = forms.CharField(label='Subject', max_length=50)
    message = forms.CharField(label='Message', max_length=500)

    def clean(self) -> dict[str, Any] | None:
        subject = self.cleaned_data.get('subject')
        message = self.cleaned_data.get('message')
        if message == subject:
            raise forms.ValidationError('message and subject are same')

    def clean_name(self) -> str:
        name = self.cleaned_data.get('name')
        if 'a' in name:
            raise forms.ValidationError('a can not be in your name')
        return name


class MessageForm(forms.ModelForm):# you have to change forms.forms to forms.ModelForm
    # subject = forms.CharField(label='Subject', max_length=50)
    # message = forms.CharField(widget=forms.Textarea, label='Message')
    # email = forms.EmailField(label='Email')
    # name = forms.CharField(label='Name', max_length=10 )

    class Meta:
        model = Message
        fields = ('subject', 'message','name', 'email' , 'age')
        widgets = {
            "name" : forms.TextInput(attrs={'class':'form-control'
                                            ,'placeholder':'Enter your name'}),
            "email" : forms.EmailInput(attrs={'class':'form-control'}),
            "subject" : forms.TextInput(attrs={'class':'form-control'}),
            "message" : forms.Textarea(attrs={'class':'form-control'}),
            "age" : forms.NumberInput(attrs={'class':'form-control'}),
        }



class ArticleCreateForm(forms.ModelForm):
    class Meta:
        model = article
        fields = ('title', 'content', 'category', 'image')
        widgets = {
            "title": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter an engaging title...'}),
            "content": forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your post content here...'}),
            "category": forms.Select(attrs={'class': 'form-control'}),
            "image": forms.FileInput(attrs={'class': 'form-control'}),
        }