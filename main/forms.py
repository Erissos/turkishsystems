from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from .models import ProjectRequest


class ProjectRequestForm(forms.ModelForm):
    class Meta:
        model = ProjectRequest
        fields = [
            "full_name",
            "email",
            "company_name",
            "phone",
            "request_type",
            "budget_range",
            "timeline",
            "project_scope",
            "systems_note",
            "wants_portal_access",
        ]


class SignUpForm(forms.Form):
    full_name = forms.CharField(max_length=150)
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    def clean_username(self):
        username = self.cleaned_data["username"].strip()
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("Bu kullanıcı adı zaten kayıtlı.")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Bu e-posta ile zaten bir hesap bulunuyor.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            self.add_error("password2", "Şifreler eşleşmiyor.")
        return cleaned_data

    def save(self):
        full_name = self.cleaned_data["full_name"].strip()
        user = User.objects.create_user(
            username=self.cleaned_data["username"].strip(),
            email=self.cleaned_data["email"].strip().lower(),
            password=self.cleaned_data["password1"],
            first_name=full_name,
        )
        return user


class SignInForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        self.user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username", "").strip()
        password = cleaned_data.get("password", "")
        if username and password:
            self.user = authenticate(username=username, password=password)
        if username and password and self.user is None:
            raise forms.ValidationError("Kullanıcı adı veya şifre hatalı.")
        return cleaned_data

    def get_user(self):
        return self.user