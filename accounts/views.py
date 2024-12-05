from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from accounts.forms import *
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.template.loader import render_to_string
from django.core.mail import send_mail
from accounts.models import User
from django.conf import settings
from .simplifier import check_captcha
from accounts.signals import user_registered
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
# set the site key and min score as global variables to use it in multiple methods
site_key = settings.RECAPTCHA_PUBLIC_KEY
min_score = settings.RECAPTCHA_REQUIRED_SCORE

# @login_required(login_url="counter:login")


class CustomizedPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomPasswordForm
    success_url = reverse_lazy('accounts:password_reset_complete')
    template_name = "register/password_reset_confirm.html"


class CustomizedPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    success_url = reverse_lazy('accounts:password_reset_done')
    template_name = "register/password_reset.html"
    email_template_name = 'register/password_reset_custom_email.text'


@require_http_methods(["GET", "POST"])
def login_view(request):

    if request.method == "POST":
        form = LoginForm(request.POST)
    else:
        form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():

            result = check_captcha(request)

            if not result.get("success") or result.get("score") < min_score:
                messages.error(
                    request, "There is a problem please try again later!")

                return redirect(reverse("accounts:login"))

            user = form.cleaned_data.get("user")
            login(request, user)
            return (redirect(reverse("content:home")))

    return render(request, "register/login.html", {
        "form": form,
        "site_key": site_key,
        "action": "login"
    })


@require_http_methods(["GET", "POST"])
def register_view(request):

    if request.method == "POST":
        form = CustomRegister(request.POST)

        if form.is_valid():

            result = check_captcha(request)
            if not result.get("success") or result.get("score") < min_score:
                messages.error(
                    request, "Recaptcha Verification Error Please Try Again!")
                return redirect(reverse("accounts:register"))

            user = form.save()
            user_registered.send(sender=User, user=user, request=request)

            messages.info(request, "You Are Registered,Please Login To Site!")
            return redirect(reverse("accounts:login"))

        else:
            return render(request, "register/register.html", {
                "form": form,
                "site_key": site_key
            })

    form = CustomRegister()

    return render(request, "register/register.html", {
        "form": form,
        "site_key": site_key
    })


def logout_view(request):

    logout(request)
    messages.info(request, "Logged Out!")
    return redirect(reverse("accounts:login"))


@require_http_methods(["GET", "POST"])
@login_required(login_url="counter:login")
def password_change(request):

    if request.method == "POST":
        form = PasswordChangeForm(request.POST)
        if form.is_valid():

            result = check_captcha(request)
            if not result.get("success") or result.get("score") < min_score:
                messages.error(
                    request, "There is a problem please try again!")
                return redirect(reverse("accounts:change_pass"))
            old_password = form.cleaned_data["old_pass"]
            new_password = form.cleaned_data["new_pass"]
            user = request.user

            if user.check_password(old_password):
                user.set_password(new_password)
                user.save()
                messages.info(request, "Password changed successfully!")
                return redirect(reverse("accounts:login"))
            else:
                form.add_error(None, "Invalid old password!")
                return redirect(reverse("accounts:change_pass"))

        else:
            return render(request, "register/password_change.html", {"form": form})
    form = PasswordChangeForm()
    return render(request, "register/password_change.html", {"form": form})
