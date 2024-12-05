from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from accounts.models import Profile
from allauth.account.adapter import DefaultAccountAdapter

# here I changed the default populate_user method which allauth uses to create the User in memory
# I defined some extra code in it to update the user's profile object(witch created by the create_profile
# receiver when the user logged in first time using google account)


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        name = data.get("name")
        picture = data.get("picture")

        # with below code,if the user's picture in google account be changed,then the picture of user's profile also will be changed in database
        if hasattr(user, "profile"):
            user.profile.name = name
            user.profile.picture = picture

        return user

    def generate_unique_username(self, txts, regex=None):
        username = txts[0] + txts[1]
        for i in txts:
            print(i)
        return username
