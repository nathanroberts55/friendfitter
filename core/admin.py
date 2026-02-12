from django.contrib import admin
from django import forms
from .models import MeasurementProfile, Fabric, Pattern, PatternSizeRequirement, Project
from .services import validate_and_convert_yardage


class PatternSizeRequirementForm(forms.ModelForm):
    required_length = forms.CharField(
        help_text="Enter yardage (e.g., '2 3/8' or '2.5').",
        label="Required Length (Yards)",
    )

    class Meta:
        model = PatternSizeRequirement
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If we are editing an existing requirement, convert inches to yardage string
        if self.instance and self.instance.pk:
            from .services import convert_inches_to_yardage

            # self.instance.required_length is stored in inches (e.g. 85.5)
            self.initial["required_length"] = convert_inches_to_yardage(
                self.instance.required_length
            )

    def clean_required_length(self):
        data = self.cleaned_data["required_length"]
        return validate_and_convert_yardage(data)


class PatternSizeRequirementInline(admin.TabularInline):
    """Allows editing sizes directly on the Pattern page."""

    form = PatternSizeRequirementForm
    model = PatternSizeRequirement
    extra = 1  # Number of empty rows to show by default
    min_num = 1  # Ensures you add at least one size


@admin.register(Pattern)
class PatternAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "is_full_length")
    list_filter = ("category",)
    inlines = [PatternSizeRequirementInline]


@admin.register(Fabric)
class FabricAdmin(admin.ModelAdmin):
    list_display = ("name", "width_inches", "length_inches", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("name",)


@admin.register(MeasurementProfile)
class MeasurementProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "last_updated")
    readonly_fields = ("last_updated",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("pattern", "recipient", "fabric", "status", "started_at")
    list_filter = ("status",)

    # This helps you select fabrics that are still available
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "fabric":
            kwargs["queryset"] = Fabric.objects.filter(status="AVAILABLE")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
