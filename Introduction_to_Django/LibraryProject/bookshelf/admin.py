from django.contrib import admin
from .models import Book

class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "publication_year")  # show these columns in list
    search_fields = ("title", "author")  # enable search bar
    list_filter = ("publication_year",)  # filter by year on right panel

admin.site.register(Book, BookAdmin)
