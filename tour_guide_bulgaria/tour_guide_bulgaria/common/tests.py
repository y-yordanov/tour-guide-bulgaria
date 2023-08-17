import unittest
from django.core.exceptions import ValidationError
from tour_guide_bulgaria.common.validators import validate_only_letters


class ValidateOnlyLettersValidatorTests(unittest.TestCase):
    def test_when_chars_are_not_letters__expect_to_raise(self):
        with self.assertRaises(ValidationError):
            validate_only_letters('sym#bol')

    def test_when_chars_are_valid__expect_to_do_nothing(self):
        validate_only_letters('symbol')


