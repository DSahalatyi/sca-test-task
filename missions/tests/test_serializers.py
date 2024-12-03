from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase

from cats.models import Cat
from missions.models import Target, Mission
from missions.serializers import (
    TargetSerializer,
    MissionSerializer,
    MissionUpdateSerializer, TargetUpdateSerializer,
)


class TestTargetSerializer(APITestCase):
    def setUp(self):
        self.mission = Mission.objects.create(is_complete=False)
        self.target = Target.objects.create(
            name="Target 1", mission=self.mission, is_complete=False, country="Country"
        )

    def test_validate_target_status_target_complete(self):
        self.target.is_complete = True
        self.target.save()

        with self.assertRaises(ValidationError):
            TargetSerializer.validate_target_status(self.target)

    def test_validate_target_status_mission_complete(self):
        self.mission.is_complete = True
        self.mission.save()

        with self.assertRaises(ValidationError):
            TargetSerializer.validate_target_status(self.target)


class TestMissionSerializer(APITestCase):
    def setUp(self):
        self.mission = Mission.objects.create(is_complete=False)

    def test_target_names_unique_in_mission(self):
        data = {
            "is_complete": False,
            "targets": [
                {"name": "Target 1", "country": "Country", "notes": "Notes", "is_complete": False},
                {"name": "Target 1", "country": "Country", "notes": "Notes", "is_complete": False},
            ],
        }

        serializer = MissionSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("targets", serializer.errors)
        self.assertEqual(
            serializer.errors["targets"][0],
            "Target names must be unique within a mission.",
        )

    def test_create_target_on_completed_mission(self):
        self.mission.is_complete = True
        self.mission.save()

        data = {
            "is_complete": True,
            "targets": [
                {"name": "Target 1", "notes": "Some notes", "is_complete": False}
            ],
        }

        serializer = MissionSerializer(data=data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)


class TestMissionUpdateSerializer(APITestCase):
    def setUp(self):
        self.cat = Cat.objects.create(name="Test", years_of_experience=10, breed="Persian", salary=100)
        self.mission = Mission.objects.create(is_complete=False)
        self.target = Target.objects.create(
            name="Target 1", mission=self.mission, is_complete=False, country="Country", notes="Notes"
        )

    def test_validate_assignee_on_completed_mission(self):
        self.mission.is_complete = True
        self.mission.save()

        data = {
            "targets": [
                {"name": "Target 1", "notes": "Updated notes", "is_complete": True}
            ],
            "assignee": self.cat.id
        }

        serializer = MissionUpdateSerializer(instance=self.mission, data=data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_update_target_notes_on_completed_target(self):
        self.target.is_complete = True
        self.target.save()

        data = {
            "targets": [
                {"name": "Target 1", "notes": "Updated notes", "is_complete": True}
            ]
        }

        serializer = TargetUpdateSerializer(instance=self.mission, data=data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_update_target_notes_on_completed_mission(self):
        self.mission.is_complete = True
        self.mission.save()

        data = {
            "targets": [
                {"name": "Target 1", "notes": "Updated notes", "is_complete": True}
            ]
        }

        serializer = TargetUpdateSerializer(instance=self.mission, data=data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
