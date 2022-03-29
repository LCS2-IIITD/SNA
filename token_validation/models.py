from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.
class Tokens(models.Model):
    token = models.CharField(max_length = 10, unique = True)
    active = models.BooleanField(default = False)

    def __str__(self):
        return str(self.token) 

    class Meta:
        verbose_name_plural = "Tokens"
        verbose_name = "Token"
        permissions = (("can_bulk_uploaded", "Can bulk uploaded token CSV"),)

class Subscription(models.Model):
    email = models.EmailField(unique=True)

class AccountManager(BaseUserManager):
    def create_user(self, first_name, email, token, last_name = None, password = None):
        if not email:
            raise ValueError('All users must have a valid E-Mail address.')
        

        user = self.model(
            first_name = first_name,
            last_name = last_name,
            email = self.normalize_email(email),
            token = Tokens.objects.get(id=token),
        )

        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_superuser(self, first_name, email, token, last_name = None, password = None):
        user = self.create_user(first_name, email, token, last_name, password)
        user.is_admin = True
        user.is_superuser = True
        user.save(using = self._db)
        return user

class Account(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length = 96)
    last_name = models.CharField(max_length = 96, null = True)
    email = models.EmailField(
        verbose_name = 'email address',
        max_length = 255,
        unique = True
    )
    token = models.ForeignKey(Tokens, on_delete=models.CASCADE, related_name = 'foreign_key_token', unique=True)
    is_active = models.BooleanField(default = True)
    is_admin = models.BooleanField(default = False)
    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['token', 'first_name']

    def __str__(self):
        return str(self.first_name) + ' ' + str(self.last_name) + ' ' + self.email
    
    def is_staff(self):
        return self.is_admin