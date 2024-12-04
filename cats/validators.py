import requests
from rest_framework.exceptions import ValidationError


class CatApiValidator:
    api_url = "https://api.thecatapi.com/"
    version = "v1"

    def validate_breed(self, breed: str):
        breed_id = self.get_breed_id(breed)

        res = requests.get(f"{self.api_url}{self.version}/breeds/{breed_id}")
        if res.status_code != 200:
            raise ValidationError(f"Invalid breed: {breed}")


    @staticmethod
    def get_breed_id(breed: str) -> str:
        if len(breed.split()) == 2:
            prefix = breed.split()[0]
            breed = breed.split()[1]
            return (prefix[0] + breed[:3]).lower()
        else:
            return breed[:4].lower()


class NumberValidator:
    def validate_positive(self, field_name: str, value: int | float):
        if value < 0:
            raise ValidationError(f"{field_name} value must be positive!")