from allauth.account.adapter import DefaultAccountAdapter
from .models import User

class AccountAdapter(DefaultAccountAdapter):

    def get_phone(self, user):
        return (str(user.phone_number), user.phone_number_verified)

    def set_phone(self, user, phone, verified=False):
        user.phone_number = phone
        user.phone_number_verified = verified
        user.save()

    def set_phone_verified(self, user, phone):
        if (user.phone_number != phone):
            return
        user.phone_number_verified = True
        user.save()


    def get_user_by_phone(self, phone):
        try:
            return User.objects.get(phone_number=phone)
        except User.DoesNotExist:
            return None

    def send_verification_code_sms(self, user, phone, code, **kwargs):
        # integrate your SMS provider here
        with open("verification_code.txt", "w") as f:
            f.write(
                f"Your code is: {code}"
        )
