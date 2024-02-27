from django.urls import path
from .views import leaderboard_view

urlpatterns = [
    path("", leaderboard_view, name="leaderboard"),
]
