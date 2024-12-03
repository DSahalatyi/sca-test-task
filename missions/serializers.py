from django.db import transaction
from rest_framework import serializers

from missions.models import Target, Mission


class TargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = ("name", "country", "notes", "is_complete")

    def validate_notes(self, value):
        target = self.instance
        self.validate_target_status(target)
        return value

    @staticmethod
    def validate_target_status(target):
        if target.is_complete:
            raise serializers.ValidationError(
                "Cannot update notes because the target is completed."
            )
        if target.mission.is_complete:
            raise serializers.ValidationError(
                "Cannot update notes because the mission is completed."
            )


class TargetUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = ("name", "notes", "is_complete")


class TargetListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = ("id", "name", "country", "notes", "is_complete")


class MissionSerializer(serializers.ModelSerializer):
    targets = TargetSerializer(many=True)

    class Meta:
        model = Mission
        fields = "__all__"

    def create(self, validated_data):
        with transaction.atomic():
            targets_data = validated_data.pop("targets")
            mission = Mission.objects.create(**validated_data)

            if mission.is_complete:
                raise serializers.ValidationError(
                    "Cannot assign targets to a completed mission."
                )

            for target in targets_data:
                Target.objects.create(mission=mission, **target)
            return mission


class MissionListSerializer(MissionSerializer):
    targets = TargetListSerializer(many=True)


class MissionUpdateSerializer(MissionSerializer):
    targets = TargetUpdateSerializer(many=True)

    def validate_assignee(self, value):
        mission = self.instance

        if mission.is_complete:
            raise serializers.ValidationError("Cannot assign cats to a complete mission.")

        return value

    def update(self, instance, validated_data):
        targets_data = validated_data.pop("targets", [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        for target_data in targets_data:
            target_name = target_data.get("name")
            if target_name:
                target = Target.objects.get(name=target_name, mission=instance)
                target.is_complete = target_data.get("is_complete", target.is_complete)
                updated_notes = target_data.get("notes", target.notes)
                if updated_notes != target.notes:
                    TargetSerializer.validate_target_status(target)
                    target.notes = updated_notes
                target.save()

        return instance
