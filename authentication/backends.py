

from .models import User


class MyBackend(object):
    def authenticate(self, username=None, password=None):
        if username is None or password is None:
            return None
        user = User.objects.get(username=username, password=password)
        if user:
            return user
        return None
        # Check the username/password and return a User.