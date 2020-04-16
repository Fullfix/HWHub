from django.contrib import admin
from .models import Homework, HomeworkImage, Grade, Subject, Book, New
from .forms import BookUploadForm

# Register your models here.

@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
	list_display = ('publisher', 'grade', 'subject',
		'book', 'number', 'publication_date', 'like_count', 'dislike_count')
	list_display_links = ('number', 'publisher')
	list_filter = ('publication_date',)

	def like_count(self, obj):
		return str(obj.likes.count())

	def dislike_count(self, obj):
		return str(obj.likes.count())

@admin.register(HomeworkImage)
class HomeworkImageAdmin(admin.ModelAdmin):
	list_display = ('homework', 'index', 'image')

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
	list_display = ('grade',)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
	list_display = ('grade', 'name', 'full_name')
	list_display_links = ('grade', 'name')

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
	list_display = ('name', 'full_name',
		'slug', 'subject', 'grade', 'image', 'types')
	list_display_links = ('name', 'full_name', 'slug')
	form = BookUploadForm

	def grade(self, obj):
		return str(obj.subject.grade.grade)

@admin.register(New)
class NewAdmin(admin.ModelAdmin):
	list_display = ('publisher', 'summary', 'description', 'publication_date')
	list_filter = ('publication_date',)