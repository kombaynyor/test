from django.db import models
from django.urls import reverse


# Создание БД, все тимы палей смотри на Django.FuN
# !!!! Обязательное наследование от models
class News(models.Model):
    title = models.CharField(max_length=150, verbose_name='Наименование')
    content = models.TextField(blank=True, verbose_name='Наименование')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    # photos/%Y/%m/%d/ означат что все фотки будут отсортированы по году дню и месяцу и созданны соответсвующие папки
    # со вложеиями
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Обновлено', blank=True)
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    # Если основная модель объявлена ниже то вот так, если выше то без скобочек
    category = models.ForeignKey('Category', on_delete=models.PROTECT,verbose_name='Категория')
    view = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('view_news', kwargs={"pk": self.pk})

    # Возвращаю запись столбцом БД
    def __str__(self):
        return self.title

    # "Настройка отображения БД" в админке
    class Meta:
        # меняет название News на необходимое
        verbose_name = 'Новость'
        # меняет множественно чисто News
        verbose_name_plural = 'Новости'
        # опредяляем сортировку записи в админке
        ordering = ['-created_at']

class Category(models.Model):
    title = models.CharField(max_length=150, db_index=True, verbose_name='Наименование категории')

    # Регламентированное

    def get_absolute_url(self):
        return reverse('category', kwargs={"category_id": self.pk})

    def __str__(self):
        return self.title

    class Meta:
        # меняет название News на необходимое
        verbose_name = 'Категория'
        # меняет множественно чисто News
        verbose_name_plural = 'Категории'
        # опредяляем сортировку записи в админке
        ordering = ['title']
