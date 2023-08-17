
from datetime import date

from django import test as django_test
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.urls import reverse

from tour_guide_bulgaria.accounts.models import Profile
from tour_guide_bulgaria.web.models import Sight, Category

UserModel = get_user_model()


class ProfileTests(django_test.TestCase):
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
        return self.client.get(reverse('profile details', kwargs={'pk': profile.pk}))

    def __get_response_for_registered_profile(self):
        return self.client.get(reverse('show dashboard', ))

    def test_profile_create__when_first_name_contain_only_letters__expect_success(self):
        _, profile = self.__create_valid_user_and_profile()
        profile.save()
        self.assertIsNotNone(profile.pk)

    def test_profile_create__when_first_name_contains_a_digit__expect_to_fail(self):
        first_name = 'Ivan1'
        profile = Profile(
            first_name=first_name,
            last_name=self.VALID_PROFILE_DATA['last_name'],
            age=self.VALID_PROFILE_DATA['age'],
            profile_image=self.VALID_PROFILE_DATA['profile_image']
        )

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()

        self.assertIsNotNone(context.exception)

    def test_profile_create__when_first_name_contains_a_dollar_sign__expect_to_fail(self):
        first_name = '$Ivan'
        profile = Profile(
            first_name=first_name,
            last_name=self.VALID_PROFILE_DATA['last_name'],
            age=self.VALID_PROFILE_DATA['age'],
            profile_image=self.VALID_PROFILE_DATA['profile_image']
        )

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()

        self.assertIsNotNone(context.exception)

    def test_profile_create__when_first_name_contains_a_space__expect_to_fail(self):
        first_name = 'Iv an'
        profile = Profile(
            first_name=first_name,
            last_name=self.VALID_PROFILE_DATA['last_name'],
            age=self.VALID_PROFILE_DATA['age'],
            profile_image=self.VALID_PROFILE_DATA['profile_image']
        )

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()

        self.assertIsNotNone(context.exception)

    def test_expect_correct_template_for_registered_profile(self):
        _, profile = self.__create_valid_user_and_profile()
        self.__get_response_for_registered_profile()
        self.assertTemplateUsed('accounts/home_with_profile.html')

    def test_create_profile__when_profile_with_same_first_and_last_name_exists_error(self):
        self.__create_valid_user_and_profile()

        response = self.client.post(
                reverse('register'),
                data=self.VALID_PROFILE_DATA,
            )

        profiles = Profile.objects.filter(**self.VALID_PROFILE_DATA)
        self.assertEqual(1, len(profiles))

    def test_when_opening_not_existing_profile__expect_404(self):
        response = self.client.get(reverse('profile details', kwargs={
            'pk': 1,
        }))

        self.assertEqual(404, response.status_code)

    def test_expect_correct_template(self):
        _, profile = self.__create_valid_user_and_profile()
        self.__get_response_for_profile(profile)
        self.assertTemplateUsed('accounts/profile_details.html')

    def test_when_user_is_owner__expect_is_owner_to_be_true(self):
        _, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)

        response = self.__get_response_for_profile(profile)

        self.assertTrue(response.context['is_owner'])

    def test_when_user_is_not_owner__expect_is_owner_to_be_false(self):
        _, profile = self.__create_valid_user_and_profile()
        credentials = {
            'username': 'testuser2',
            'password': '123456789',
        }

        self.__create_user(**credentials)

        self.client.login(**credentials)

        response = self.__get_response_for_profile(profile)

        self.assertFalse(response.context['is_owner'])

    def test_when_sights__expect_user_sights_count_to_be_1(self):
        user, profile = self.__create_valid_user_and_profile()
        category = self.__create_category()
        self.__create_sight_for_user(user, category)
        response = self.__get_response_for_profile(profile)

        self.assertEqual(1, response.context['user_sights_count'])

    def test_when_user_has_sights__expect_to_return_only_users_sights(self):
        user, profile = self.__create_valid_user_and_profile()
        credentials = {
            'username': 'testuser2',
            'password': '123456789',
        }

        user2 = self.__create_user(**credentials)
        category = self.__create_category()
        sight_first_user = Sight.objects.create(
            **self.VALID_SECOND_SIGHT_DATA,
            category=category,
            user=user,
        )
        self.__create_sight_for_user(user2, category)
        response = self.__get_response_for_profile(profile)

        self.assertListEqual(
            [sight_first_user],
            response.context['user_sights'],
        )

    def test_when_user_has_no_sights__sights_should_be_empty(self):
        _, profile = self.__create_valid_user_and_profile()

        response = self.__get_response_for_profile(profile)
        self.assertListEqual(
            [],
            response.context['user_sights'],
        )

    def test_edit_profile_example(self):
        user, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)

        self.client.post(
            reverse('edit profile', kwargs={
                'pk': profile.pk,
            }),
            data=None
        )


