from django.contrib import admin

# Register your models here.
from quickstart.models import Blog, Author, Entry, Student


class StudentAdmin(admin.ModelAdmin):
    list_display = ('id','name')
admin.site.register(Blog, StudentAdmin)
admin.site.register(Author)
#admin.site.register(Student)
# admin.site.register(Entry)

class EntryAdmin(admin.ModelAdmin):
    list_display = ('headline', 'body_text', 'blog')
admin.site.register(Entry, EntryAdmin)

#username:admin
#password:python@123



class YourModelAdmin(admin.ModelAdmin):
    list_display = ('id','field3_without_link', 'last_name')

    def field3_without_link(self, obj):
        return obj.first_name
    field3_without_link.short_description = 'first_name'  # Customize column header

admin.site.register(Student, YourModelAdmin)