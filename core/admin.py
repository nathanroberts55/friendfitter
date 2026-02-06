from django.contrib import admin
from .models import MeasurementProfile, Fabric, Pattern, PatternSizeRequirement, Project


class PatternSizeRequirementInline(admin.TabularInline):
    """Allows editing sizes directly on the Pattern page."""

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
