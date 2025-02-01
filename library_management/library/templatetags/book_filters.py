# library/templatetags/book_filters.py

from django import template

register = template.Library()

print("book_filters.py is loaded")

@register.filter
def get_book_id(borrowed_books, book):
    return borrowed_books.filter(book=book).first().id if borrowed_books.filter(book=book).exists() else None
