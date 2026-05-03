from django.urls import path

from . import views
from .views import contact_api


urlpatterns = [
    path("", views.home, name="home"),
    path("api/contact/", contact_api, name="contact_api"),
]
