
from datetime import date

from django import test as django_test
from django.contrib.auth import get_user_model
from django.urls import reverse

from tour_guide_bulgaria.accounts.models import Profile
from tour_guide_bulgaria.web.models import Sight, Category, SightComment

UserModel = get_user_model()


class SightTests(django_test.TestCase):
    VALID_USER_CREDENTIALS = {
        'username': 'testuser',
        'password': '12345678',
    }

    VALID_PROFILE_DATA = {
        'first_name': 'Test',
        'last_name': 'User',
        'age': 18,
        'about': 'I am Test User',
        'profile_image': 'ads.jpg',
    }

    VALID_SIGHT_DATA = {
        'name_of_sight': 'Pirin',
        'location': 'Bulgaria',
        'description': 'Beautiful',
        'post_date': date(2023, 7, 27),
        'image': 'ads.jpg',
    }

    VALID_SECOND_SIGHT_DATA = {
            'name_of_sight': 'Rila',
            'location': 'Bulgaria',
            'description': 'Woow',
            'post_date': date(2023, 7, 28),
            'image': 'abc.jpg',
        }

    VALID_CATEGORY_DATA = {
        'name': 'Nature',
    }

    def __create_user(self, **credentials):
        return UserModel.objects.create_user(**credentials)

    def __create_category(self, **credentials):
        return Category.objects.create(**credentials)

    def __create_valid_user_and_profile(self):
        user = self.__create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(
            **self.VALID_PROFILE_DATA,
            user=user,
        )
        return (user, profile)

    def __create_sight_for_user(self, user, category):
        sight = Sight.objects.create(
            **self.VALID_SIGHT_DATA,
            category=category,
            user=user,
        )
        return sight

    def __get_response_for_profile(self, profile):
        return self.client.get(reverse('sight details', kwargs={'pk': profile.pk}))

    def __get_response_for_sight(self, sight):
        return self.client.get(reverse('sight details', kwargs={'pk': sight.pk}))

    def test_expect_correct_template(self):
        _, profile = self.__create_valid_user_and_profile()
        self.__get_response_for_profile(profile)
        self.assertTemplateUsed('web/sight_details.html')

    def test_when_user_is_owner_of_the_sight__expect_is_owner_to_be_true(self):
        user, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        category = self.__create_category()
        sight = self.__create_sight_for_user(user, category)

        response = self.__get_response_for_sight(sight)

        self.assertTrue(response.context['is_owner'])

    def test_when_user_is_not_owner_of_the_sight__expect_is_owner_to_be_false(self):
        user, profile = self.__create_valid_user_and_profile()
        credentials = {
            'username': 'testuser2',
            'password': '123456789',
        }
        category = self.__create_category()
        sight = self.__create_sight_for_user(user, category)
        self.__create_user(**credentials)
        self.client.login(**credentials)

        response = self.__get_response_for_sight(sight)

        self.assertFalse(response.context['is_owner'])

    def test_when_no_sight_likes__expect_likes_count_to_be_0(self):
        user, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        category = self.__create_category()
        sight = self.__create_sight_for_user(user, category)
        response = self.__get_response_for_sight(sight)
        print(response)

        self.assertEqual(0, response.context['likes_count'])

    def test_when_no_sight_comments__expect_comments_count_to_be_0(self):
        user, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        category = self.__create_category()
        sight = self.__create_sight_for_user(user, category)
        response = self.__get_response_for_sight(sight)
        comments = sight.sight_comments.count()

        self.assertEqual(comments, response.context['comments_count'])

    def test_edit_sight_example(self):
        user, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        category = self.__create_category()
        sight = self.__create_sight_for_user(user, category)

        self.client.post(
            reverse('edit sight', kwargs={
                'pk': sight.pk,
            }),
            data=None
        )

