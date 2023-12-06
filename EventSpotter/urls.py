from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('login', views.login_view, name="login"),
    path('search', views.search_view, name="search"),
    path('results', views.results_view, name="results"),
    path('logout', views.logout_view, name="logout"),
    path('about', views.about_view, name="about"),
    path('register', views.register_view, name="register"),
    path('add', views.add_view, name="add"),
    path('delete/<int:event_id>', views.delete_view, name="delete"),
    path('saved', views.events_saved_view, name='saved'),
    path('location', views.location_view, name='location')
]
