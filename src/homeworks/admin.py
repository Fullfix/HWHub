from django.contrib import admin
from .models import Homework, HomeworkImage, Grade, Subject, Book, New

# Register your models here.

admin.site.register(Homework)
admin.site.register(HomeworkImage)
admin.site.register(Grade)
admin.site.register(Subject)
admin.site.register(Book)
admin.site.register(New)