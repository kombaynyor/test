from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse

from .models import News, Category
from .forms import NewsForm
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView


class HomeNews(ListView):
    model = News
    template_name = 'news/home_news_list.html'
    # название для использования в шаблонах
    context_object_name = 'news'
    # extra_context = {'title' : 'Главная'}
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category')


class NewsByCategory(ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    allow_empty = False

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True).select_related('category')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs['category_id'])
        return context


# здесь обозначаем какие представления у нас будут
# request обязательный параметр
# def index(request):
# получаем данные из моделе и отправляем рендериться в шаблон
# Важно! В соответсвии с документацией все шаблоны храняться в папке templates
# Джанго ищет там в первую очеред в templates должна быть вложенна папка с названием модели
# + Нет гемора с путями
# news = News.objects.order_by('-created_at')
# context = {
#   'news': news,
#   'title': 'Список новостей',
# }
# return render(request, 'news/index.html', context)


def get_category(request, category_id):
    news = News.objects.filter(category_id=category_id)
    category = Category.objects.get(pk=category_id)
    return render(request, 'news/category.html', {'news': news, 'category': category, })


class ViewNews(DetailView):
    model = News
    context_object_name = 'news_item'
    # template_name = 'news/news_detail.html'
    # pk_url_kwarg = 'news_id'


# def add_news(request):
#   if request.method == 'POST':
#      form = NewsForm(request.POST)
#     if form.is_valid():
#        # print(form.cleaned_data)
#       #news = News.objects.create(**form.cleaned_data)
#      news = form.save()
#     return redirect(news)
# else:
#   form = NewsForm()
# return render(request,'news/add_news.html', {'form' : form})

class CreateNews(CreateView):
    form_class = NewsForm
    template_name = 'news/add_news.html'
    # success_url = reverse_lazy('home')
