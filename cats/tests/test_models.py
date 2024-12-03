from django.test import TestCase

from cats.models import Cat


class CatModelTests(TestCase):
    def test_cat_str(self):
        cat_dict = {
            "name": "Test",
            "years_of_experience": 2,
            "breed": "Persian",
            "salary": 100,
        }

        cat = Cat.objects.create(**cat_dict)
        self.assertEqual(
            str(cat),
            f"{cat_dict['name']} ({cat_dict['breed']}. Exp: {cat_dict['years_of_experience']}. ${cat_dict['salary']})",
        )
