from allauth.account.signals import user_signed_up
from accounts.signals import user_registered
from django.dispatch import receiver
from .models import Profile
import requests
from django.core.files import File
import io

# when the user logged in using google api,the allauth will create the
# user instance for the user(If already not exist) and then will sent
# the signal with name of "user_signed_up",I used this signal to create
#  the profile object for user too.


@receiver(user_signed_up)
def create_profile(sender, **kwargs):
    user = kwargs["user"]
    social_account = user.socialaccount_set.first()
    if social_account:
        name = social_account.extra_data["name"]
        # get the user's picture url from social account's extra_data
        # to download and save it in profile object
        picture_url = social_account.extra_data["picture"]
        get_picture = requests.get(picture_url)
        profile = Profile.objects.create(
            user_id=user, name=name)

        if get_picture.status_code == 200:
            picture_file = File(io.BytesIO(get_picture.content))
            profile.picture.save(name + ".jpg", picture_file)

        profile.save()


@receiver(user_registered)
def complete_user_registering(sender, **kwargs):
    user = kwargs.get("user")
    name = user.username.capitalize()
    profile = Profile.objects.create(name=name, user_id=user)
    profile.save()
    print(f"the {name}'s profile created")
