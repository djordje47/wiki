from django.urls import path

from . import views
app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path('search', views.search, name="search"),
    path('create-entry', views.createEntry, name='create-entry'),
    path('random-page', views.randomPage, name="random-entry"),
    path('<str:title>', views.page, name="page"),
    path('edit-entry/<str:title>', views.editEntry, name='edit-entry'),
]
