from django import forms
from .models import MeasurementProfile


class MeasurementForm(forms.ModelForm):
    class __clipp__:  # Helper to avoid repetition
        field_class = "input input-bordered w-full"

    class Meta:
        model = MeasurementProfile
        fields = [
            "bust_chest",
            "waist",
            "hips",
            "shoulder_width",
            "inseam",
            "height_total",
        ]
        # Friendly labels for your friends
        labels = {
            "bust_chest": "Bust/Chest",
            "waist": "Waist",
            "hips": "Hips",
            "shoulder_width": "Shoulder",
            "inseam": "Inseam",
            "height_total": "Total Height",
        }

        # Guidance text to ensure they measure correctly
        help_texts = {
            "bust_chest": "Measure around the fullest part of your chest/bust.",
            "waist": "The narrowest part of your torso, usually above the belly button.",
            "hips": "The widest part of your lower body, usually around your seat.",
            "shoulder_width": "Measure from the bony point of one shoulder to the other.",
            "inseam": "From the crotch to your ankle bone.",
            "height_total": "From the top of your head to the floor.",
        }
        widgets = {
            "bust_chest": forms.NumberInput(attrs={"class": "input input-bordered"}),
            "waist": forms.NumberInput(attrs={"class": "input input-bordered"}),
            "hips": forms.NumberInput(attrs={"class": "input input-bordered"}),
            "shoulder_width": forms.NumberInput(
                attrs={"class": "input input-bordered"}
            ),
            "inseam": forms.NumberInput(attrs={"class": "input input-bordered"}),
            "height_total": forms.NumberInput(attrs={"class": "input input-bordered"}),
        }
