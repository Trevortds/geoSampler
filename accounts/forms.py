from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import UserAttributeSimilarityValidator, MinimumLengthValidator, \
    CommonPasswordValidator, NumericPasswordValidator, validate_password
from django.contrib.auth.validators import UnicodeUsernameValidator

User = get_user_model()


class GuestForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Email",
                "id": "form_full_name",
                }
        ))


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Username",
                "id": "form_full_name",
                }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
                "class": "form-control",
                "placeholder": "Password",
                "id": "form_full_name",
                }
        )
    )


class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Username",
                "id": "form_full_name",
                }
        ), validators=[UnicodeUsernameValidator()]
    )

    email = forms.EmailField(widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Email",
                "id": "form_full_name",
                }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
                "class": "form-control",
                "placeholder": "Password",
                "id": "form_full_name",
                }),
    )
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={
                "class": "form-control",
                "placeholder": "Password",
                "id": "form_full_name",
                }
    ))

    def clean_username(self):
        username = self.cleaned_data.get("username")
        qs = User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("User already exists with given email")
        return email

    def clean(self):
        data = self.cleaned_data
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password != password2:
            raise forms.ValidationError("Passwords do not match")
        validate_password(password)

        return data


class PasswordChangeForm(forms.Form):

    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
                "class": "form-control",
                "placeholder": "Password",
                "id": "form_full_name",
                }),
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
                "class": "form-control",
                "placeholder": "Password",
                "id": "form_full_name",
                }),
    )
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={
                "class": "form-control",
                "placeholder": "Password",
                "id": "form_full_name",
                }
    ))

    def __init__(self, *args, **kwargs):
        self.username = kwargs.pop('username')
        super(PasswordChangeForm, self).__init__(*args, **kwargs)

    def clean(self):
        data = self.cleaned_data
        user = authenticate(username=self.username, password=self.cleaned_data.get("old_password"))
        if user is None:
            raise forms.ValidationError("Old password does not match")
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password != password2:
            raise forms.ValidationError("Passwords do not match")
        validate_password(password)

        return data