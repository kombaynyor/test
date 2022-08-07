from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse

from .models import News, Category
from .forms import NewsForm, UserRegisterForm , UserLoginForm
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from .utils import MyMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.contrib.auth import login, logout

from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, 'news/register.html', {'form' : form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'news/login.html', {'form' : form})
def user_logout(request):
    logout(request)
    return redirect('login')
def test(request):
    objects = ['joh1', 'paul2', 'georde3', 'ringo4','paul5','john6','ringo7']
    paginator = Paginator(objects,2)
    page_num = request.GET.get('page', 1)
    page_objects = paginator.get_page(page_num)
    return render(request, 'news/test.html', {'page_obj': page_objects})


class HomeNews(ListView, MyMixin):
    model = News
    template_name = 'news/home_news_list.html'
    # название для использования в шаблонах
    context_object_name = 'news'
    # extra_context = {'title' : 'Главная'}
    allow_empty = False
    mixin_prop = 'hello word'
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_upper('Главная страница')
        context['mixin_prop'] = self.get_prop()
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category')


class NewsByCategory(ListView, MyMixin):
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

class CreateNews(LoginRequiredMixin, CreateView):
    form_class = NewsForm
    template_name = 'news/add_news.html'
    #login_url = '/admin/'
    raise_exception = True
    # success_url = reverse_lazy('home')
