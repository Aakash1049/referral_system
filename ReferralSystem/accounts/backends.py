# accounts/backends.py

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class EmailAuthBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        print("in custom authenthicate")
        try:
            # Look for user by email
            user = get_user_model().objects.get(email=email)
            # Check if the password is correct
            print(user)
            if user.check_password(password):
                return user
        except get_user_model().DoesNotExist:
            print("user does not exist")
            return None
