from django.urls import path
from . import views

urlpatterns = [
    path("_dashboard/", views.dashboard, name="dashboard"),
    path("<slug:product>/", views.landing, name="landing"),
    path("<slug:product>/convert/", views.convert, name="convert"),
    path("<slug:product>/maintenance/", views.maintenance, name="maintenance"),
]
