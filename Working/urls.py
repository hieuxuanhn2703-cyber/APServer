from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("", views.web_view, name="web"),
    path("list/", views.list_view, name="list"),
    path("edit/<int:row_id>/", views.edit_view, name="edit"),
]