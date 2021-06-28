from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.home, name="home"),
    path('notes/', views.notes, name="notes"),
    path('homework/', views.homework, name="homework"),
    path('note-delete/<int:id>/', views.notedelete, name="note_delete"),
    path('delete-homework/<int:id>/',
         views.deletehomework, name="delete_homework"),
    path('note-update/<int:id>/', views.noteupdate, name="note_update"),
    path('update-homework/<int:id>/',
         views.updatehomework, name="update_homework"),
    path('mark-homework/<int:id>/', views.markhomework, name="mark_homework"),
    path('note-detail/<int:pk>/', views.NoteDetailView.as_view(), name="note_detail"),
    path('youtube/', views.youtube, name="youtube"),
    path('todo/', views.todo, name="todo"),
    path('delete-todo/<int:id>/', views.deletetodo, name="deletetodo"),
    path('update-todo/<int:id>/', views.updatetodo, name="update_todo"),
    path('mark-todo/<int:id>/', views.marktodo, name="marktodo"),
    path('books/', views.books, name="books"),
    path('dictionary/', views.dictionary, name="dictionary"),
    path('wiki/', views.wiki, name="wiki"),
    path('conversion/', views.conversion, name="conversion"),
    path('register/', views.register, name="register"),
    path('profile/', views.profile, name="profile"),
    path('login/', auth_views.LoginView.as_view(template_name = 'dashboard/login.html'), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name = 'dashboard/logout.html'), name="logout"),
]
