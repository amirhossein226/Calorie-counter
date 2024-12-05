from django.conf import settings
import requests


def check_captcha(request):
    secret_key = settings.RECAPTCHA_PRIVATE_KEY
    recaptcha_response = request.POST.get("g-recaptcha-response")
    data = {
        "secret": secret_key,
        "response": recaptcha_response
    }
    recaptcha_verification = requests.post(
        "https://www.google.com/recaptcha/api/siteverify", data=data)

    result = recaptcha_verification.json()
    print(result)
    return result
