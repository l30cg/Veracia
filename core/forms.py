from django import forms
from .models import User, Tag, Category

class CategoryForm(forms.Form):
   name = forms.CharField(label="Enter Name: ", max_length=60)

class TagForm(forms.Form):
   name = forms.CharField(label="Enter tag: ", max_length=60)

class UserForm(forms.Form):
   username = forms.CharField(label="Enter username:", max_length=150)
   email = forms.EmailField(label="Enter email:", max_length=150)
   password = forms.CharField(label="Enter password:", max_length=150, widget=forms.PasswordInput())
   first_name = forms.CharField(label="Enter first name:", max_length=150)
   last_name = forms.CharField(label="Enter last name:", max_length=150)
   # biography = forms.CharField(label="Enter biography:", max_length=150, widget=forms.Textarea())

class PostForm(forms.Form):
   title = forms.CharField(label="Enter title: ", max_length=120)
   description = forms.CharField(label="Enter description: ", max_length=255)
   user = forms.ModelChoiceField(label="Enter user:", queryset=User.objects.all())
   categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all())
   tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all())
