from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    @classmethod
    def phone_normalise(cls, phone_number: str):
        if phone_number == '':
            return None
        digits = ''.join(filter(str.isdigit, phone_number))
        if len(digits) == 11:
            formatted_number = f'+7 ({digits[1:4]}) {digits[4:7]}-{digits[7:9]}-{digits[9:]}'
        elif len(digits) == 10:
            formatted_number = f'+7 ({digits[0:3]}) {digits[3:6]}-{digits[6:8]}-{digits[8:]}'
        else:
            return None
        return formatted_number

    def create_user(self, phone_number=None, password=None, email=None, **kwargs):
        if not email and not phone_number:
            return ValueError('you shout input email or phone_number')
        email = self.normalize_email(email) if email else None
        phone_number = self.phone_normalise(phone_number) if phone_number else None
        user = self.model(email=email, phone_number=phone_number, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number=None, password=None, email=None, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        return self.create_user(phone_number, password, email, **kwargs)