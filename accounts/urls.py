from django.urls import path, reverse_lazy
from .import views
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetCompleteView
from django.contrib.auth.forms import PasswordResetForm

app_name = "accounts"

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),
    path("change_pass/", views.password_change, name="change_pass"),
    path("password-reset/", views.CustomizedPasswordResetView.as_view(),
         name="password_reset"),
    path("password-reset/done/",
         PasswordResetDoneView.as_view(template_name="register/password_reset_done.html"), name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>/",
         views.CustomizedPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("password-reset-complete/", PasswordResetCompleteView.as_view(
        template_name="register/password_reset_complete.html"), name="password_reset_complete")
]
