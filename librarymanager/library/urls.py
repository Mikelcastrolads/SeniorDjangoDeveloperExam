from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/register/', views.register, name='register'),

    # Books URLs
    path('', views.BookListView.as_view(), name='book_list'),
    path('book/<uuid:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    path('books/<uuid:pk>/borrow/', views.BorrowBookView.as_view(), name='borrow_book'),
    path('books/<uuid:pk>/return/', views.ReturnBookView.as_view(), name='return_book'),
    path('book/add/',  views.BookCreateView.as_view(), name='add_book'),
    path('book/<uuid:pk>/edit/', views.BookUpdateView.as_view(), name='edit_book'),
    path('book/<uuid:pk>/delete/',  views.BookDeleteView.as_view(), name='delete_book'),

    # Author URLs
    path('authors/', views.AuthorListView.as_view(), name='author_list'),
    path('author/<uuid:pk>/', views.AuthorDetailView.as_view(), name='author_detail'),
    path('author/add/', views.AuthorCreateView.as_view(), name='add_author'),
    path('author/<uuid:pk>/edit/', views.AuthorUpdateView.as_view(), name='edit_author'),
    path('author/<uuid:pk>/delete/', views.AuthorDeleteView.as_view(), name='delete_author'),

    # Genre URLs
    path('genres/', views.GenreListView.as_view(), name='genre_list'),
    path('genre/<uuid:pk>/', views.GenreDetailView.as_view(), name='genre_detail'),
    path('genre/add/', views.GenreCreateView.as_view(), name='add_genre'),
    path('genre/<uuid:pk>/edit/', views.GenreUpdateView.as_view(), name='edit_genre'),
    path('genre/<uuid:pk>/delete/', views.GenreDeleteView.as_view(), name='delete_genre'),
]