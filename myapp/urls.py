from django.urls import path

from . import views
from .views import contact_api, contact_page
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path("", views.home, name="home"),
    path("api/contact/", contact_api, name="contact_api"),
    path("contact/", contact_page, name="contact"),
    path("blog/create/", views.blog_create, name="blog_create"),
    path("blog/edit/<slug:slug>/", views.blog_edit, name="blog_edit"),
    path("blog/", views.blog_list, name="blog_list"),
    path("blog/<slug:slug>/", views.blog_detail, name="blog_detail"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
