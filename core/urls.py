from django.urls import path
from . import views

urlpatterns = [
    path("", views.matchmaker_dashboard, name="matchmaker_dashboard"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.account_logout, name="logout"),
    path(
        "results/pattern/<int:pattern_id>/fabric/<int:fabric_id>/",
        views.matchmaker_results,
        name="matchmaker_results",
    ),
    path("my-measurements/", views.measurement_update, name="measurement_update"),
]
