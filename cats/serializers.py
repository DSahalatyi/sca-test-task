from rest_framework import serializers

from cats.models import Cat
from cats.validators import CatApiValidator, NumberValidator


class CatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cat
        fields = "__all__"

    def validate(self, data):
        errors = {}

        validator = CatApiValidator()
        try:
            validator.validate_breed(data.get("breed"))
        except serializers.ValidationError as e:
            errors["breed"] = e.detail

        validator = NumberValidator()
        field = "years_of_experience"
        try:
            validator.validate_positive(field, data.get(field))
        except serializers.ValidationError as e:
            errors[field] = e.detail

        field = "salary"
        try:
            validator.validate_positive(field, data.get(field))
        except serializers.ValidationError as e:
            errors[field] = e.detail

        if errors:
            raise serializers.ValidationError(errors)

        return super().validate(data)


class CatUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cat
        fields = ("salary",)
