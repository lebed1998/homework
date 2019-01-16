from django.contrib import admin
from .models import Film, Review


@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    pass


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass

