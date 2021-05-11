from os import path

from django import forms
from django.contrib.auth.models import User

from comic.models import Directory


class InitialSetupForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

    def clean(self):
        form_data = self.cleaned_data
        if form_data["password"] != form_data["password_confirm"]:
            raise forms.ValidationError("Passwords do not match.")
        if len(form_data["password"]) < 8:
            raise forms.ValidationError("Password is too short")
        return form_data


class AccountForm(forms.Form):
    username = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control disabled", "readonly": True}),
    )
    email = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(
        required=False, widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    password_confirm = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    def clean_email(self):
        data = self.cleaned_data["email"]
        user = User.objects.get(username=self.cleaned_data["username"])
        if data == user.email:
            return data
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError("Email Address is in use")
        return data

    def clean(self):
        form_data = self.cleaned_data
        if form_data["password"] != form_data["password_confirm"]:
            raise forms.ValidationError("Passwords do not match.")
        if len(form_data["password"]) < 8 & len(form_data["password"]) != 0:
            raise forms.ValidationError("Password is too short")
        return form_data


class AddUserForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

    def clean_username(self):
        data = self.cleaned_data["username"]
        if User.objects.filter(username=data).exists():
            raise forms.ValidationError("This username Exists.")
        return data

    def clean_email(self):
        data = self.cleaned_data["email"]
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError("Email Address is in use")
        return data

    def clean(self):
        form_data = self.cleaned_data
        if form_data["password"] != form_data["password_confirm"]:
            raise forms.ValidationError("Passwords do not match.")
        if len(form_data["password"]) < 8:
            raise forms.ValidationError("Password is too short")
        return form_data


class EditUserForm(forms.Form):
    username = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control disabled", "readonly": True}),
    )
    email = forms.EmailField(widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(
        required=False, widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    allowed_to_read = forms.ChoiceField(choices=Directory.Classification.choices)

    @staticmethod
    def get_initial_values(user):
        out = {"username": user.username, "email": user.email, "allowed_to_read": user.usermisc.allowed_to_read}
        return out

    def clean_password(self):
        data = self.cleaned_data["password"]
        if len(data) < 8 & len(data) != 0:
            raise forms.ValidationError("Password is too short")
        return data


class DirectoryEditForm(forms.Form):
    classification = forms.ChoiceField(choices=Directory.Classification.choices)
