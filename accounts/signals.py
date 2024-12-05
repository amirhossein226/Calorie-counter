from django.dispatch import Signal


# register a signal which will propagate when the user registered in website,and I will use it in receivers.py
user_registered = Signal()
