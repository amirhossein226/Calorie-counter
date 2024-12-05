from django import template
from django.conf import settings
from django.utils.safestring import mark_safe


register = template.Library()


@register.simple_tag
def re_token_script(action):
    return mark_safe(f"""
    <script src='https://www.google.com/recaptcha/api.js?render={settings.RECAPTCHA_PUBLIC_KEY}'></script>
    <script>
    grecaptcha.ready(function () {{
        var captcha_execute = function () {{
            grecaptcha.execute('{settings.RECAPTCHA_PUBLIC_KEY}', {{ action: '{action}' }}).then(function (token) {{
                document.querySelectorAll('input.recaptcha-hidden-input').forEach(function (element) {{
                    element.value = token;
                }});
            }});
        }};

        captcha_execute();
        setInterval(captcha_execute, 1200);
    }});
    </script>
    """)
