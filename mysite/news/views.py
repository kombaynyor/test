from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse

from .models import News, Category
from .forms import NewsForm

# здесь обозначаем какие представления у нас будут
# request обязательный параметр
def index(request):
    # получаем данные из моделе и отправляем рендериться в шаблон
    # Важно! В соответсвии с документацией все шаблоны храняться в папке templates
    # Джанго ищет там в первую очеред в templates должна быть вложенна папка с названием модели
    # + Нет гемора с путями
    news = News.objects.order_by('-created_at')
    context = {
        'news': news,
        'title': 'Список новостей',
    }
    return render(request, 'news/index.html', context)


def get_category(request, category_id):
    news = News.objects.filter(category_id=category_id)
    category = Category.objects.get(pk=category_id)
    return render(request, 'news/category.html', {'news' : news,  'category': category,})

def view_news(request,news_id):
    #news_item = News.objects.get(pk=news_id)
    news_item = get_object_or_404(News, pk=news_id)
    return render(request,'news/view_news.html', {'news_item': news_item})


def add_news(request):
    if request.method == 'POST':
        pass
    else:
        form = NewsForm()
    return render(request,'news/add_news.html', {'form' : form})