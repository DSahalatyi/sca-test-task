from django.db import models

from cats.models import Cat


class Mission(models.Model):
    assignee = models.ForeignKey(
        Cat,
        related_name="missions",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    is_complete = models.BooleanField(default=False)


class Target(models.Model):
    name = models.CharField(max_length=127)
    country = models.CharField(max_length=63)
    notes = models.TextField()
    is_complete = models.BooleanField(default=False)
    mission = models.ForeignKey(
        Mission, related_name="targets", on_delete=models.CASCADE
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "mission"], name="unique_target_per_mission"
            )
        ]
