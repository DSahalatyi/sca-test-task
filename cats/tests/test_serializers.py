from unittest.mock import patch
from rest_framework.exceptions import ValidationError

from cats.models import Cat
from cats.serializers import CatSerializer, CatUpdateSerializer
from django.test import TestCase


class CatSerializerTest(TestCase):

    def setUp(self):
        self.cat_data = {
            "name": "Test Cat",
            "breed": "Siamese",
            "years_of_experience": 5,
            "salary": 50000,
        }

    @patch("cats.validators.CatApiValidator.validate_breed")
    def test_valid_breed(self, mock_validate_breed):
        mock_validate_breed.return_value = None

        serializer = CatSerializer(data=self.cat_data)
        if not serializer.is_valid():
            self.fail(f"Serializer failed validation: {serializer.errors}")

    @patch("cats.validators.CatApiValidator.validate_breed")
    def test_invalid_breed(self, mock_validate_breed):
        mock_validate_breed.side_effect = ValidationError("Invalid breed")

        serializer = CatSerializer(data=self.cat_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("breed", serializer.errors)
        self.assertEqual(serializer.errors["breed"], ["Invalid breed"])

    def test_cat_serializer_invalid_positive_fields(self):
        # Test invalid salary or years_of_experience (negative values)
        self.cat_data["salary"] = -50000
        serializer = CatSerializer(data=self.cat_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("salary", serializer.errors)

        self.cat_data["salary"] = 50000
        self.cat_data["years_of_experience"] = -5
        serializer = CatSerializer(data=self.cat_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("years_of_experience", serializer.errors)


class CatUpdateSerializerTest(TestCase):

    def setUp(self):
        self.cat = Cat.objects.create(name="Test Cat", breed="Siamese", years_of_experience=5, salary=50000)

    def test_cat_update_serializer_valid(self):
        update_data = {"salary": 55000}
        serializer = CatUpdateSerializer(instance=self.cat, data=update_data, partial=True)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["salary"], 55000)

    def test_cat_update_serializer_invalid_salary(self):
        update_data = {"salary": -50000}
        serializer = CatUpdateSerializer(instance=self.cat, data=update_data, partial=True)
        self.assertFalse(serializer.is_valid())
        self.assertIn("salary", serializer.errors)