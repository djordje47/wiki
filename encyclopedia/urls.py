from django.urls import path

from . import views
app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path('search', views.search, name="search"),
    path('<str:title>', views.page, name="page"),
    path('random-page', views.randomPage, name="random-page"),
]
