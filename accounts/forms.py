from django.contrib.auth import authenticate, get_user_model
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from accounts.models import Profile
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm

UserModel = get_user_model()


class CustomRegister(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={"class": "t-cen input-1 holder-1", "placeholder": "Your Email"}))
    username = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={"class": "t-cen input-1 holder-1", "placeholder": "username", "autocomplete": "off"}))
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "t-cen input-1 holder-1", "placeholder": "Password"}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "t-cen input-1 holder-1", "placeholder": "Password conf"}))

    class Meta(UserCreationForm.Meta):
        model = UserModel
        fields = ["email", "username", "password1", "password2"]

    def clean_username(self):
        username = self.cleaned_data.get("username")
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        if user:
            user.email = self.cleaned_data.get("email")
            user.username = self.cleaned_data.get("username")
            if commit:
                user.save()
        else:
            self.cleaned_data["wrong"] = "Please Insert Valid value!"
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(required=True, widget=forms.EmailInput(
        attrs={"class": "t-cen input-1 holder-1", "placeholder": "Enter Your Email", "autofocus": True, "id": "login_email"}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={"class": "t-cen input-1 holder-1", "placeholder": "Password", "id": "login_password"}), required=True)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if password and email:
            valid_user = authenticate(username=email, password=password)
            if not valid_user:
                raise ValidationError(
                    "User With This Email/Password Does Not Exist!", code="check_error")
            cleaned_data["user"] = valid_user
            return cleaned_data
        else:
            raise ValidationError(
                "The Email/Password must be Insert!", code="value_error")


class PasswordChangeForm(forms.Form):

    old_pass = forms.CharField(widget=forms.PasswordInput, required=True)
    new_pass = forms.CharField(widget=forms.PasswordInput, required=True)
    new_pass_conf = forms.CharField(
        widget=forms.PasswordInput, required=True)

    def clean(self):
        cleaned_data = super().clean()
        old_pass = self.cleaned_data.get("old_pass")
        new_pass = self.cleaned_data.get("new_pass")
        new_pass_confirm = self.cleaned_data.get("new_pass_conf")

        if new_pass and new_pass_confirm and old_pass:
            if new_pass == new_pass_confirm:
                return cleaned_data
            else:
                raise ValidationError(
                    "new password and new password's confirmation must be same!", code="not_same")

        else:
            raise ValidationError(
                "All Of Fields Must Be Filled!", code="required")


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "t-cen input-1 holder-1", "placeholder": "amir222@gmail.com", "autocomplete": "off"}))


class CustomPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={"class": "t-cen input-1 holder-1 li-martl-1", "placeholder": "Password"}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 't-cen input-1 holder-1 li-martl-1', 'placeholder': 'Password Confirmation'}))
