
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone

# Create your models here.


# class CustomUserManager(BaseUserManager):
#     use_in_migrations = True
#
#     def _create_user(self, phone_number, password, **extra_fields):
#         """Create and save a User with the given email and password."""
#         if not phone_number:
#             raise ValueError('The given email must be set')
#
#         user = self.model(phone_number=phone_number, **extra_fields)
#         errors = dict()
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#     def create_user(self, phone_number, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', False)
#         extra_fields.setdefault('is_superuser', False)
#         return self._create_user(phone_number, password, **extra_fields)
#
#     def create_superuser(self, phone_number, password, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#
#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must have is_staff=True.')
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True.')
#
#         return self._create_user(phone_number, password, **extra_fields)

class APIUserManager(BaseUserManager):
    """Custom user manager."""
    use_in_migrations = True


    def create_user(self, email, password=None, **kwargs):
        """Create a user."""
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            first_name=kwargs.get("first_name", ""),
            last_name=kwargs.get("last_name", ""),
            phone_number=kwargs.get("phone_number", ""),
            address=kwargs.get("address", ""),
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password):
        """Create a superuser."""
        user = self.create_user(email, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class APIUser(AbstractBaseUser, PermissionsMixin):
    """Custom user class."""

    USERNAME_FIELD = "email"

    USER_TYPE_ADMIN = "admin"

    # username field not used, only here to make django-rest-auth work
    username = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=False, unique=True)
    first_name = models.CharField("first name", max_length=50)
    last_name = models.CharField("last name", max_length=50)
    phone_number = models.CharField(max_length=20, verbose_name='phone number')
    address = models.TextField(null=True, blank=True)

    is_staff = models.BooleanField(
        "staff status",
        default=False,
        help_text="Designates whether the user can log into this admin site.",
    )
    is_active = models.BooleanField(
        "active",
        default=True,
        help_text="Designates whether this user should be treated as active. "
        "Deselect this instead of deleting accounts.",
    )
    create_time = models.DateTimeField("date joined", default=timezone.now)


    objects = APIUserManager()

    class Meta:
        """Model meta data."""

        verbose_name = "user"
        verbose_name_plural = "users"

    def get_full_name(self):
        """Get full name."""
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Get short name."""
        return self.first_name

