from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from datetime import datetime


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('reader', 'Reader'),
        ('librarian', 'Librarian'),
        ('admin', 'Admin'),
    ]
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='reader')

    groups = models.ManyToManyField(
        Group,
        related_name="customuser_groups",
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    is_recommended = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='book_images/', blank=True, null=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Borrow(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(default=datetime.now)  # Manually eset the default
    return_date = models.DateTimeField(null=True, blank=True)  # Nullabl, for when the book is returned
    returned = models.BooleanField(default=False)  # Tracks if the book has been returned

    def __str__(self):
        return f"{self.book.title} borrowed by {self.user.username}"
