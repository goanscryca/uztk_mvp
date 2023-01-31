from django.urls import path

from uztk.users.views import (
    user_detail_view,
    user_redirect_view,
    user_update_view,
    lock_control
)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),
    path("lock/<int:lock_id>", view=lock_control, name="lock-control")
]
