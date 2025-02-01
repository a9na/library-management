from django.urls import path
from . import views

urlpatterns = [
    # Home page
    path('', views.home, name='home'),

    # Books-related URLs
    path('books/', views.book_list, name='book_list'),  # List of all books
    path('add_book/', views.add_book, name='add_book'),  # Add a new book (for librarians)
    path('books/<int:id>/', views.book_detail, name='book_detail'),  # Detail of a specific book
    path('book_detail/<int:book_id>/', views.book_detail, name='book_detail'),
    path('borrow_book/<int:book_id>/', views.borrow_book, name='borrow_book'),  # Borrow a specific book
    path('return_book/<int:borrow_id>/', views.return_book, name='return_book'),  # Return a borrowed book

    # User-related URLs
    path('register/', views.register, name='register'),  # User registration
    path('login/', views.user_login, name='login'),  # Login page
    path('logout/', views.user_logout, name='logout'),  # Logout page

    # Dashboard URLs
    path('librarian_dashboard/', views.librarian_dashboard, name='librarian_dashboard'), # Librarian dashboard
    path('reader_dashboard/', views.reader_dashboard, name='reader_dashboard'),  # Reader dashboard
]
