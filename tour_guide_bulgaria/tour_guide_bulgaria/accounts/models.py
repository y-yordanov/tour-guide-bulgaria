from django.contrib.auth import models as auth_models
from django.contrib.auth.models import User
from tour_guide_bulgaria.accounts.managers import AppUserManager
from tour_guide_bulgaria.common.validators import validate_only_letters
from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models
from cloudinary import models as cloudinary_models


class AppUser(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    USERNAME_MAX_LENGTH = 25
    PROFILE_IMAGE_UPLOAD_TO_DIR = 'profiles/'

    username = models.CharField(
        max_length=USERNAME_MAX_LENGTH,
        unique=True,
    )

    date_joined = models.DateTimeField(
        auto_now_add=True,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    USERNAME_FIELD = 'username'

    objects = AppUserManager()


class Profile(models.Model):
    FIRST_NAME_MIN_LENGTH = 2
    FIRST_NAME_MAX_LENGTH = 15
    LAST_NAME_MIN_LENGTH = 2
    LAST_NAME_MAX_LENGTH = 15
    AGE_MIN_VALUE = 10
    PROFILE_IMAGE_UPLOAD_TO_DIR = 'profiles/'

    first_name = models.CharField(
        verbose_name='First Name',
        max_length=FIRST_NAME_MAX_LENGTH,
        validators=(
            MinLengthValidator(FIRST_NAME_MIN_LENGTH),
            validate_only_letters,
        )
    )

    last_name = models.CharField(
        verbose_name='Last Name',
        max_length=LAST_NAME_MAX_LENGTH,
        validators=(
            MinLengthValidator(LAST_NAME_MIN_LENGTH),
            validate_only_letters,
        )
    )

    age = models.IntegerField(
        verbose_name='Age',
        validators=(
            MinValueValidator(AGE_MIN_VALUE),
        )
    )

    about = models.TextField(
        verbose_name='About Me',
    )

    profile_image = cloudinary_models.CloudinaryField(
        'image',
    )

    user = models.OneToOneField(
        AppUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
