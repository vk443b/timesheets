import imp
from django.db import models
from django.contrib.auth.models import BaseUserManager, PermissionsMixin
from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import RegexValidator
# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, email, phone_number, first_name, last_name, username, password=None, superuser=0, staff=False):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not phone_number:
            raise ValueError('Users must have a mobile number')

        user = self.model(
            email=email,
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            username=username,
            is_superuser=superuser,
            is_staff=staff,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone_number, first_name, last_name, username, password=None,):
        """
        Creates and saves a superuser with the given email, phone number and password.
        """
        user = self.create_user(
            email=email,
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            superuser=1,
            staff=True,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

    def get_queryset(self):
        return super().get_queryset().filter(is_superuser=1, is_staff=True)


class ClientUserManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_superuser=0, is_staff=False)



class Users(AbstractBaseUser,PermissionsMixin):
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, verbose_name="email", blank=False, unique=True)
    username = models.CharField(max_length=100, verbose_name="username", blank=False, unique=True)
    phone_number = models.CharField(
        max_length=16,
        validators=[
        RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message="Phone number must be entered in the format '+123456789'. Up to 15 digits allowed."
        ),
        ],
    )
    date_joined = models.DateTimeField(auto_now_add=True, db_column="created at")
    password = models.CharField(max_length=255,)
    is_staff = models.BooleanField('staff status',
                                   default=False,
                                   help_text='Designates whether the user can log into this admin site.', )
    is_superuser = models.IntegerField(default=0, blank=True)
    is_active = models.IntegerField(default=1)

    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number', 'email']
    USERNAME_FIELD = 'username'

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.username}"

    class Meta:
        verbose_name = 'Admin'
        verbose_name_plural = 'Admins'


class ClientUser(Users):
    objects = ClientUserManager()
    class Meta:
        proxy = True
        verbose_name = 'User'
        verbose_name_plural = 'Users'
