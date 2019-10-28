from django.db import models

# Create your models here.

class Publisher(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    website = models.URLField()

class Author(models.Model):
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=40, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    def __str__(self):
        return self.last_name + ", " + self.first_name

class Book(models.Model):
    title = models.CharField(max_length=30, blank=True, null=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, blank=True, null=True)
    publication_date = models.DateField(null=True, blank=True)
    edition = models.IntegerField(null=True, blank=True)
    imagen = models.CharField(max_length=100, null=True, blank=True)
    copies = models.IntegerField(null = True, blank=True)
