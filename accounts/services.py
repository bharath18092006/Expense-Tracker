from django.contrib.auth.models import User


class AccountService:
    @staticmethod
    def get_account(user: User) -> User:
        return User.objects.get(pk=user.pk)
