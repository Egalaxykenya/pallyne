from pally.models import PallyneUser

class EmailAuthenticationBackend(object):
    """
    Authenticates user's using email addresses

    """
    def authenticate(self, request, username=None, password=None):
        try:
            user = PallyneUser.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None


    def get_user(self, user_id):
        try:
            return PallyneUser.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
