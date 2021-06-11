from django.urls import path     
from . import views

urlpatterns = [
path('', views.index),
path('index', views.index),
path('register', views.register),
path('login', views.login),
path('home', views.home),
path('search', views.search),
path('info/<int:id>', views.info),
path('profile/<int:user_id>', views.profile),
path('edit_box/<int:box_id>', views.edit_box),
path("info/<int:book_id>/edit_box", views.edit_box),
path('edit_user/<int:user_id>', views.edit_user),
path('delete/<int:user_id>', views.delete),
path('delete_box/<int:box_id>', views.delete_box),
path('add_box', views.add_box),
path('logout', views.logout),
path('view', views.view),
]