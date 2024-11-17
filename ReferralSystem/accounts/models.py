from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, name, mobile, city, password=None, referral_code=None):
        if not email or not name or not mobile or not city:
            raise ValueError("All mandatory fields must be filled.")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, mobile=mobile, city=city, referral_code=referral_code)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, mobile, city, password=None):
        user = self.create_user(email=email, name=name, mobile=mobile, city=city, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=15)
    city = models.CharField(max_length=255)
    referral_code = models.CharField(max_length=10, blank=True, null=True)
    referrer = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL, related_name='referees')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'mobile', 'city']

    def __str__(self):
        return self.email
