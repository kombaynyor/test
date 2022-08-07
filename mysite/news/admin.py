from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe

from .models import News, Category
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class NewsAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = News
        fields = '__all__'

class NewsAdmin(admin.ModelAdmin):
    form = NewsAdminForm
    # Показываем что должно отображаться в админке
    list_display = ('id', 'category', 'title', 'created_at', 'updated_at', 'is_published', 'get_photo')
    # Ссылки на необходимые поля
    list_display_links = ('id', 'title')
    # Возможность поиска по модели
    search_fields = ('title', 'id')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'category')
    fields = ('category', 'content', 'photo', 'is_published', 'view', 'get_photo', 'title', 'created_at', 'updated_at')
    readonly_fields = ('get_photo', 'view', 'created_at', 'updated_at')
    save_on_top = True
    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="75">')
        else:
            return 'Фото не установлено'
    get_photo.short_description = 'Миниатюра'


class CategotyAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)


# Регистрация всего этого
# ВАЖНО!!! первым всегда идет модель, после настройки

admin.site.register(News, NewsAdmin)
admin.site.register(Category, CategotyAdmin)
admin.site.site_title = 'Управление новостями'
admin.site.site_header = 'Управление новостями'