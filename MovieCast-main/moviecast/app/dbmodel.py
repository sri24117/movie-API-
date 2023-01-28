# import datetime
from django.db import models

class User(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=250)
    email = models.CharField(max_length=250)
    password = models.CharField(max_length=250)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "UsersTable"

class Session(models.Model):
    token = models.TextField()
    email = models.CharField(max_length=255)
    created_at = models.BigIntegerField()
    expiry_at = models.BigIntegerField()
    class Meta:
        db_table = "SessionsTable"

class Movie(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    runtime = models.IntegerField()
    language = models.CharField(max_length=255)
    tagline = models.CharField(max_length=255)

    class Meta:
        db_table = "MoviesTable"

class Cast(models.Model):
    id = models.IntegerField(primary_key=True)
    movieid = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=255)
    dob = models.DateField()

    class Meta:
        db_table = "CastsTable"

