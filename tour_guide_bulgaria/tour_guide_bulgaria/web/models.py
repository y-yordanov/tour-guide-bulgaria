from django.contrib.auth import get_user_model
from django.db import models
from cloudinary import models as cloudinary_models


UserModel = get_user_model()


class Category(models.Model):
    CATEGORY_MAX_LEN = 25

    name = models.CharField(
        max_length=CATEGORY_MAX_LEN,
    )

    def __str__(self):
        return self.name


class Sight(models.Model):
    CATEGORY_MAX_LEN = 25
    NAME_MAX_LEN = 30
    LOCATION_MAX_LEN = 100
    IMAGE_UPLOAD_TO_DIR = 'destinations/'

    name_of_sight = models.CharField(
        verbose_name='Name of Sight',
        max_length=NAME_MAX_LEN,
        unique=True,
    )

    location = models.CharField(
        verbose_name='Location',
        max_length=LOCATION_MAX_LEN,
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        # choices=CATEGORIES
    )

    description = models.TextField(
        verbose_name='Description',
    )

    post_date = models.DateTimeField(
        auto_now_add=True,
    )

    pros = models.TextField(
        verbose_name='Pros',
        null=True,
        blank=True,
    )

    cons = models.TextField(
        verbose_name='Cons',
        null=True,
        blank=True,
    )

    image = cloudinary_models.CloudinaryField(
        'image',
    )

    # image = models.ImageField(
    #     upload_to=IMAGE_UPLOAD_TO_DIR,
    #     verbose_name='Image',
    # )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return '%s - %s' % (self.name_of_sight, self.user)


class SightComment(models.Model):
    MAX_BODY_LENGTH = 500

    sight = models.ForeignKey(
        Sight,
        related_name='sight_comments',
        on_delete=models.CASCADE,
        blank=True,
        null=False,
    )

    body = models.TextField()

    publication_date_and_time = models.DateTimeField(
        auto_now_add=True,
        auto_now=False,
        blank=True,
        null=False,
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return '%s - %s' % (self.sight.name_of_sight, self.user)


class SightLike(models.Model):
    sight = models.ForeignKey(
        Sight,
        on_delete=models.CASCADE,
        null=False,
        blank=True,
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )