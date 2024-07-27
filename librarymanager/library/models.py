import uuid
from django.db import models 
from django.contrib.auth.models import User


class BaseModel(models.Model): 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='%(class)s_created', on_delete=models.SET_NULL, null=True)
    updated_by = models.ForeignKey(User, related_name='%(class)s_updated', on_delete=models.SET_NULL, null=True)

    class Meta:
        abstract = True
    
class Genre(models.Model):
    genre_id    = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name        = models.CharField(max_length=100)
    BaseModel

    def __str__(self):
        return self.name

class Author(models.Model):
    author_id   = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name        = models.CharField(max_length=255)
    biography   = models.TextField()
    nationality = models.CharField(max_length=100)
    BaseModel

    def __str__(self):
        return self.name
    
class Book(models.Model):
    STATUS = [
        ('available', 'Available'),
        ('borrowed', 'Borrowed'),
    ]

    book_id             = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    title               = models.CharField(max_length=255)
    author              = models.ForeignKey(Author, on_delete=models.CASCADE)
    publication_year    = models.PositiveIntegerField()
    isbn                = models.CharField(max_length=13, unique=True)
    genre               = models.ManyToManyField(Genre)
    status              = models.CharField(max_length=10, choices=STATUS, default='available')
    BaseModel

    class Meta:
        permissions = [
            ("can_manage_books", "Can manage books"),
            ("can_manage_authors", "Can manage authors"),
            ("can_manage_genres", "Can manage genres"),
        ]

    def __str__(self):
        return self.title
     
    
class Borrow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_at = models.DateTimeField(auto_now_add=True)
    returned_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} borrowed {self.book}"