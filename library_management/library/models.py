from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPES = [
        ('client', 'Client'),
        ('privileged', 'Privileged User'),
        ('admin', 'Administrator'),
    ]
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='client')

    # Resolving the reverse accessor conflict for 'groups' and 'user_permissions'
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Unique reverse relation name for groups
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # Unique reverse relation name for user_permissions
        blank=True
    )

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    description = models.TextField()
    isbn = models.CharField(max_length=13, blank=True, null=True)  # ISBN field (optional)
    available = models.BooleanField(default=True)  # Boolean field to track availability
    image = models.ImageField(upload_to='book_images/', blank=True, null=True)  # Image field (optional)

    def __str__(self):
        return self.title



class Borrow(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} borrowed {self.book.title}"

