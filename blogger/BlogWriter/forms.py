from django import forms
from .models import BlogPost
class Register(forms.Form):
    username=forms.CharField(max_length=150,label="Username")
    email=forms.EmailField(max_length=100,label="Email")
    password=forms.CharField(widget=forms.PasswordInput,max_length=128,label="Password")
    confirm_password=forms.CharField(widget=forms.PasswordInput,max_length=128,label="Confirm Password")
    def clean(self):
        cleaned_data=super().clean()
        password=cleaned_data.get('password')
        confirm_password=cleaned_data.get('confirm_password')
        if password!=confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data
class Login(forms.Form):
    username=forms.CharField(max_length=150,label="Username")
    password=forms.CharField(widget=forms.PasswordInput,max_length=128,label="Password")
class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content']  # Add any other fields as needed
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }