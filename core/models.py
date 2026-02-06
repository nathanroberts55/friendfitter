from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

# Common validator to ensure measurements are positive and non-zero
pos_val = [MinValueValidator(0.01)]


class MeasurementProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="measurement_profile"
    )

    # We use null=True and blank=True so the profile can be created
    # as soon as the user logs in via OAuth, even before they provide data.
    bust_chest = models.DecimalField(
        max_digits=5, decimal_places=2, validators=pos_val, null=True, blank=True
    )
    waist = models.DecimalField(
        max_digits=5, decimal_places=2, validators=pos_val, null=True, blank=True
    )
    hips = models.DecimalField(
        max_digits=5, decimal_places=2, validators=pos_val, null=True, blank=True
    )
    shoulder_width = models.DecimalField(
        max_digits=5, decimal_places=2, validators=pos_val, null=True, blank=True
    )
    inseam = models.DecimalField(
        max_digits=5, decimal_places=2, validators=pos_val, null=True, blank=True
    )
    height_total = models.DecimalField(
        max_digits=5, decimal_places=2, validators=pos_val, null=True, blank=True
    )

    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Measurements for {self.user.username}"


class Fabric(models.Model):
    STATUS_CHOICES = [
        ("AVAILABLE", "Available"),
        ("IN_PROGRESS", "In Progress"),
        ("SCRAP", "Scrap Pile"),
    ]

    name = models.CharField(max_length=200)
    # image = models.ImageField(
    #     upload_to="fabrics/", help_text="Photo of the second-hand fabric"
    # )
    length_inches = models.DecimalField(
        max_digits=7, decimal_places=2, validators=pos_val
    )
    width_inches = models.DecimalField(
        max_digits=7, decimal_places=2, validators=pos_val
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="AVAILABLE"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} ({self.width_inches}" x {self.length_inches}")'


class Pattern(models.Model):
    CATEGORY_CHOICES = [
        ("TOP", "Top"),
        ("BOTTOM", "Bottom"),
        ("FULL", "Full Body"),
    ]

    name = models.CharField(max_length=200)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    # envelope_image = models.ImageField(
    #     upload_to="patterns/", help_text="Photo of the back of the pattern envelope"
    # )
    is_full_length = models.BooleanField(
        default=False,
        help_text="Check if inseam matching is required (e.g., long pants)",
    )

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"


class PatternSizeRequirement(models.Model):
    pattern = models.ForeignKey(
        Pattern, on_delete=models.CASCADE, related_name="size_requirements"
    )
    size_label = models.CharField(max_length=50)

    # All body measurements now have null=True and blank=True
    max_bust = models.DecimalField(
        max_digits=5, decimal_places=2, validators=pos_val, null=True, blank=True
    )
    max_waist = models.DecimalField(
        max_digits=5, decimal_places=2, validators=pos_val, null=True, blank=True
    )
    max_hips = models.DecimalField(
        max_digits=5, decimal_places=2, validators=pos_val, null=True, blank=True
    )
    max_shoulder = models.DecimalField(
        max_digits=5, decimal_places=2, validators=pos_val, null=True, blank=True
    )
    max_inseam = models.DecimalField(
        max_digits=5, decimal_places=2, validators=pos_val, null=True, blank=True
    )

    # Fabric requirements remain required because you can't sew without fabric!
    required_width = models.DecimalField(
        max_digits=5, decimal_places=2, validators=pos_val
    )
    required_length = models.DecimalField(
        max_digits=5, decimal_places=2, validators=pos_val
    )

    def clean(self):
        """Ensures at least one body measurement is provided."""
        if not any(
            [
                self.max_bust,
                self.max_waist,
                self.max_hips,
                self.max_shoulder,
                self.max_inseam,
            ]
        ):
            raise ValidationError(
                "You must provide at least one body measurement limit for this size."
            )

    def __str__(self):
        return f"{self.pattern.name} - {self.size_label}"


class Project(models.Model):
    STATUS_CHOICES = [
        ("PLANNED", "Planned"),
        ("IN_PROGRESS", "In Progress"),
        ("COMPLETED", "Completed"),
    ]

    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="projects_received"
    )
    fabric = models.ForeignKey(Fabric, on_delete=models.SET_NULL, null=True)
    pattern = models.ForeignKey(Pattern, on_delete=models.SET_NULL, null=True)
    size_used = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PLANNED")
    notes = models.TextField(blank=True)
    started_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Auto-archive fabric to 'Scrap Pile' upon completion
        if self.status == "COMPLETED" and self.fabric:
            self.fabric.status = "SCRAP"
            self.fabric.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Project: {self.pattern.name} for {self.recipient.username}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Creates a MeasurementProfile automatically when a new User is created."""
    if created:
        MeasurementProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_measurement_profile(sender, instance, **kwargs):
    # Change 'measurementprofile' to 'measurement_profile'
    if hasattr(instance, "measurement_profile"):
        instance.measurement_profile.save()
