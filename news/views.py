from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.http import HttpResponse
from .models import News, Category
from .forms import NewsForm, UserRegisterForm, UserLoginForm
from django.contrib import messages

#Миксин чтобы не показывать кнопку добавить новость
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout



#Регистрация пользователей
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            #Чтобы сразу авторизовать пользователя, который только что зарегался
            login(request, user)
            messages.success(request, "Вы успешно зарегистрировались")
            return redirect('home')
        else:
            messages.error(request, "Ошибка регистрации")
    else:
        form = UserRegisterForm()
    return render(request, 'news/register.html', context={'form': form})

#Авторизация пользователей
def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'news/login.html', context={'form': form})


#Выход для авторизованного польщователя
def user_logout(request):
    logout(request)
    return redirect('login')
""""
def index(request):
    news = News.objects.all()
    context = {
        'news': news,
        'title': 'Список новостей',
        }
    return render(request, 'news/index.html', context)
"""
class index(ListView):
    model = News
    template_name = 'news/index.html'
    context_object_name = 'news'
    #Пагинация страниц, сколько новостей выводить
    paginate_by = 3
    #Передать свои переменные каки-то
    def get_context_data(self, *, object_list=None, **kwargs):
        #Берем контекст и переопределяем его, далее title можно использоать в html шаблоне
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context

    #Получаем только опубликованные новости(типо фильтр пишем)
    def get_queryset(self):
        return News.objects.filter(is_published=True)

"""
def get_category(request, category_id):
    news = News.objects.filter(category_id=category_id)
    category = Category.objects.get(pk = category_id)
    return render(request, 'news/category.html', {'news': news,  'category': category})
"""

class get_category(ListView):
    model = News
    template_name = 'news/category.html'
    context_object_name = 'news'
    allow_empty = False
    # Пагинация страниц, сколько новостей выводить
    paginate_by = 3
    # Получаем только опубликованные новости и те у которых выбрана категория(типо фильтр пишем)
    def get_queryset(self):
        return News.objects.filter(is_published=True, category_id=self.kwargs['category_id'])

    def get_context_data(self, *, object_list=None, **kwargs):
        #Берем контекст и переопределяем его, далее title можно использоать в html шаблоне
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get(pk=self.kwargs['category_id'])
        return context


"""def view_news(request, news_id):
    news_item = get_object_or_404(News, pk=news_id)
    return render(request, 'news/view_news.html', {'news_item': news_item})"""

class view_news(DetailView):
    model = News
    pk_url_kwarg = 'news_id'
    template_name = 'news/view_news.html'
    context_object_name = 'news_item'

"""def add_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            news = form.save()
            return redirect(news)
    else:
        form = NewsForm()
    return render(request, 'news/add_news.html', {'title': 'Добавление новости', 'form': form})"""

class add_news(LoginRequiredMixin, CreateView):
    form_class = NewsForm
    template_name = 'news/add_news.html'
    login_url = '/admin/'

    def get_context_data(self, *, object_list=None, **kwargs):
        #Берем контекст и переопределяем его, далее title можно использоать в html шаблоне
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление новости'
        return context

