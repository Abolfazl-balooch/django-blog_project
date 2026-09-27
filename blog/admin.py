from django.contrib import admin
from . import models

class FilterByTitle(admin.SimpleListFilter):
    title = 'موضوعات'
    parameter_name = 'title'
    def lookups(self, request, model_admin):
        return (
        ('template', 'تمپلت ها'),
        ('html', 'وب')
        )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(title__icontains=self.value())
        return queryset


class comment_inline(admin.TabularInline):
    model = models.Comment

# Register your models here.
@admin.register(models.article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'updated' , "show_image")
    list_display_links = ('title',)
    list_editable = ('author', )
    list_filter = ('author' , 'category', FilterByTitle)
    search_fields = ("title", "author__username", "author__email", "category__title")
    inlines = [comment_inline]
#admin.site.register(models.article)

admin.site.register(models.Category)

admin.site.register(models.Comment)

admin.site.register(models.Message)


admin.site.register(models.Like)


