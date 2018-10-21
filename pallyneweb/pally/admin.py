from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from pally.models import PallyneUser, Publisher, LearnerProfile, Subject, Course, Module
from pally.models import Authors, ReferenceBook, AssociatedDatasets, PallyneVideo

# Registering admin models in django admin

class PallyneUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'is_staff', 'is_paid', 'is_publisher']

class ModuleInline(admin.StackedInline):
    model = Module

class PallyneVideoAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('content_title',)}
    list_display = ['content_title','content_publisher', 'published_date']
    search_fields = ['content_title']

class SubjectAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

class AssociatedDatasetsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('content_title',)}
    list_display = ['content_title', 'content_publisher', 'published_date']
    search_fields = ['content_title']

class ReferenceBookAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('book_title',)}
    list_display = ['book_title', 'book_description']

class CourseAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ['title', 'subject', 'created']
    search_fields = ['title', 'overview']
    inlines = [ModuleInline]

class ModuleAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ['course', 'title', 'description']

class PublisherAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('publisher_name',)}

admin.site.register(PallyneUser, PallyneUserAdmin)
admin.site.register(Publisher, PublisherAdmin)
admin.site.register(LearnerProfile)
admin.site.register(Authors)
admin.site.register(ReferenceBook, ReferenceBookAdmin)
admin.site.register(AssociatedDatasets, AssociatedDatasetsAdmin)
admin.site.register(PallyneVideo, PallyneVideoAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Module, ModuleAdmin)
