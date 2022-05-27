from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('vocabulary.html', views.vocabulary, name="vocabulary"),
    path('view_answer.html', views.view_answer, name="view_answer"),
    path('congratulations.html', views.congratulations, name="congratulations"),
    path('options.html', views.options, name="options"),
    path('login_user.html', views.login_user, name="login_user"),
    path('logout_user.html', views.logout_user, name="logout_user"),
    path('register_user.html', views.register_user, name="register_user"),
    path('add_cards.html', views.add_cards, name="add_cards"),
    path('edit_card.html', views.edit_card, name="edit_card"),
	]