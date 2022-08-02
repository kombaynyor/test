from django.contrib import admin
from .models import News, Category


class NewsAdmin(admin.ModelAdmin):
    # Показываем что должно отображаться в админке
    list_display = ('id', 'category', 'title', 'created_at', 'updated_at', 'is_published')
    # Ссылки на необходимые поля
    list_display_links = ('id', 'title')
    # Возможность поиска по модели
    search_fields = ('title', 'id')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'category')


class CategotyAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)


# Регистрация всего этого
# ВАЖНО!!! первым всегда идет модель, после настройки

admin.site.register(News, NewsAdmin)
admin.site.register(Category, CategotyAdmin)
