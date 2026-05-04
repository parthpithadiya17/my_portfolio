from django.urls import path

from . import views
from .views import contact_api,contact_page


urlpatterns = [
    path("", views.home, name="home"),
    path("api/contact/", contact_api, name="contact_api"),
    path("contact/", contact_page, name="contact")
]
