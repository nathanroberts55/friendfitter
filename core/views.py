from .forms import MeasurementForm
from .services import get_sewable_matches
from .models import Pattern, Fabric, MeasurementProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required


def login_view(request):
    if request.user.is_authenticated:
        return redirect("measurement_update")
    return render(request, "core/login.html")


def account_logout(request) -> None:
    logout(request=request)
    return redirect("/")


@login_required
def measurement_update(request):
    # The profile is now guaranteed to exist thanks to our Signal
    profile = request.user.measurement_profile

    if request.method == "POST":
        form = MeasurementForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("measurement_update")
    else:
        form = MeasurementForm(instance=profile)

    # Check if they've actually filled it out yet for the UI prompt
    has_data = profile.bust_chest is not None

    context = {
        "form": form,
        "profile_exists": has_data,
        "last_updated": profile.last_updated,
    }
    return render(request, "core/measurement_form.html", context)


@staff_member_required
def matchmaker_dashboard(request):
    """The main selection screen."""
    # Only show available fabrics for matching
    fabrics = Fabric.objects.filter(status="AVAILABLE")
    patterns = Pattern.objects.all()

    # If the form is submitted via GET, redirect to the results URL
    pattern_id = request.GET.get("pattern")
    fabric_id = request.GET.get("fabric")

    if pattern_id and fabric_id:
        return redirect(
            "matchmaker_results", pattern_id=pattern_id, fabric_id=fabric_id
        )

    context = {
        "fabrics": fabrics,
        "patterns": patterns,
    }
    return render(request, "core/matchmaker_dashboard.html", context)


@staff_member_required
def matchmaker_results(request, pattern_id: int, fabric_id: int):
    """The results screen based on selection."""
    pattern = get_object_or_404(Pattern, pk=pattern_id)
    fabric = get_object_or_404(Fabric, pk=fabric_id)

    matches = get_sewable_matches(pattern, fabric)

    context = {
        "pattern": pattern,
        "fabric": fabric,
        "matches": matches,
    }
    return render(request, "core/matchmaker_results.html", context)
