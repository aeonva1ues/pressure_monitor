from django.urls import path, reverse_lazy
from django.contrib.auth.views import LogoutView, LoginView

from tracker.views import NotesList, NewNote

app_name = "tracker"

urlpatterns = [
    path("", NotesList.as_view(), name="list"),
    path("create/", NewNote.as_view(), name="create_note"),
    path(
        "login/",
        LoginView.as_view(template_name="mainpage.html"),
        name="login",
    ),
    path(
        "logout/",
        LogoutView.as_view(next_page=reverse_lazy("tracker:list")),
        name="logout",
    ),
]
