import uuid
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from phonenumber_field.modelfields import PhoneNumberField

from django.contrib.auth.models import AbstractUser
# Create your models here.


# Create your models here.

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta(object):
        abstract = True



class PrimaryUUIDModel(models.Model):
    # id = models.AutoField(primary_key=True,)
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    
    class Meta(object):
        abstract = True


class PrimaryUUIDTimeStampedModel(PrimaryUUIDModel, TimeStampedModel):
    class Meta(object):
        abstract = True

USER_ROLES = (
    ('customer','customer'),
    ('driver','driver')
)

class MyUserManager(BaseUserManager):
    def create_user(self, email, date_of_birth, name,  password=None, password2=None ):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
            name = name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth, name, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            date_of_birth=date_of_birth,
            name = name
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractUser):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    email = models.EmailField(
        verbose_name="email",
        max_length=255,
        unique=True,
    )
    date_of_birth = models.DateField()
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    role = models.CharField(max_length=20,choices=USER_ROLES, blank=True)
    address = models.CharField(max_length=100, null=True)
    phone_number = PhoneNumberField(blank=True, null=True)
    
    REQUIRED_FIELDS=()
    USERNAME_FIELD=('email')
    def __str__(self):
        return self.email

  