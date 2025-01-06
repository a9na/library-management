from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('books/', views.book_list, name='book_list'),
    path('add_book/', views.add_book, name='add_book'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('member_dashboard/', views.member_dashboard, name='member_dashboard'),
    path('books/<int:id>/', views.book_detail, name='book_detail'),  # Add this line
    path('borrow_book/<int:book_id>/', views.borrow_book, name='borrow_book'),
    path('return_book/<int:borrow_id>/', views.return_book, name='return_book'),
]
