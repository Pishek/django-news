from django.contrib import admin

from .models import News, Category

#Отображение новостей в админке
class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at', 'updated_at', 'category', 'is_published')
    list_display_links = ('title', 'id')
    search_fields = ('title', 'content')
    list_editable = ('is_published', )
    list_filter = ('is_published', 'category')
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('title', 'id')
    search_fields = ('title',)
#Регистрация модели, чтобыона появилась в админке и NewsAdmin - класс, который позволяет отображать
# в админке указанные поля
admin.site.register(News, NewsAdmin)
admin.site.register(Category, CategoryAdmin)