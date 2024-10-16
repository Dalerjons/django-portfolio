from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .models import Category, Cinema, Comment, Profile
from .forms import CinemaForm, LoginForm, RegisterForm, CommentForm, EditAccountForm, EditProfileForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib import messages


# Create your views here.

# def index(request):
#     cinemas = Cinema.objects.all()
#     context = {
#         'title': 'Главная страница',
#         'cinemas': cinemas
#     }
#
#     return render(request, 'cinema_page/index.html', context)
#   верни нарисуй(по запросу, куда на страницу,  что отправить)

class CinemaListView(ListView):
    model = Cinema
    context_object_name = 'cinemas'
    template_name = 'cinema_page/index.html'
    extra_context = {
        'title': 'Главная страница'
    }



# -----------------------------------------------------------------------------------------------
# Функция для получения кинофильмов по id категории
# def category_view(request, pk):
#     cinemas = Cinema.objects.filter(category_id=pk)  # Получаем фильмы по id категории
#     category = Category.objects.get(pk=pk)  # Получили саму категорию по id
#
#     context = {
#         'title': f'Категория: {category.title}',
#         'cinemas': cinemas
#     }
#
#     return render(request, 'cinema_page/index.html', context)


class CinemaListByCategory(CinemaListView):
    # Метод который вернёт фильмы по id категории
    def get_queryset(self):
        cinemas = Cinema.objects.filter(category_id=self.kwargs['pk'])
        return cinemas

    # Метод при помощи которого мы можем дополнительно что то отправлять на страницу
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        category = Category.objects.get(pk=self.kwargs['pk'])   # Категория по id
        context['title'] = f'Категория: {category.title}'
        return context




# -----------------------------------------------------------------------------------------------
# Функция для страницы кинофильма
# def cinema_view(request, pk):
#     cinema = Cinema.objects.get(pk=pk)
#     cinemas = Cinema.objects.all()[::-1][:3]
#     context = {
#         'title': f'{cinema.category}: {cinema.title}',
#         'cinema': cinema,
#         'cinemas': cinemas
#     }
#
#     return render(request, 'cinema_page/cinema_detail.html', context)


class CinemaDetail(DetailView):
    model = Cinema
    context_object_name = 'cinema'
    template_name = 'cinema_page/cinema_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        cinemas = Cinema.objects.all()[::-1][:3]
        cinema = Cinema.objects.get(pk=self.kwargs['pk'])
        cinema.views += 1
        cinema.save()
        context['title'] = f'{cinema.category}: {cinema.title}'
        context['cinemas'] = cinemas
        if self.request.user.is_authenticated:
            context['comment_form'] = CommentForm()

        context['comments'] = Comment.objects.filter(cinema=cinema)

        return context



# -----------------------------------------------------------------------------------------------
# Функция для страницы добавления видео
# def add_cinema_view(request):
#     if request.method == 'POST':
#         form = CinemaForm(request.POST, request.FILES)
#         if form.is_valid():
#             cinema = Cinema.objects.create(**form.cleaned_data)
#             cinema.save()
#             return redirect('cinema_detail', cinema.pk)
#     else:
#         form = CinemaForm()
#
#     context = {
#         'title': 'Добавить фильм',
#         'form': form
#     }
#
#     return render(request, 'cinema_page/add_cinema.html', context)


class NewCinema(CreateView):
    form_class = CinemaForm
    template_name = 'cinema_page/add_cinema.html'
    extra_context = {
        'title': 'Добавить фильм'
    }

    # Метод для добавления Автора вашему пользователю
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)



class CinemaUpdate(UpdateView):
    model = Cinema
    form_class = CinemaForm
    template_name = 'cinema_page/add_cinema.html'
    extra_context = {
        'title': 'Изменение данных фильма'
    }


class CinemaDelete(DeleteView):
    model = Cinema
    context_object_name = 'cinema'
    success_url = reverse_lazy('index')
    template_name = 'cinema_page/cinema_confirm_delete.html'

    # Метод который будит проверять Авторизован ли и является ли Автором
    def get(self, request, *args, **kwargs):
        cinema = Cinema.objects.get(pk=self.kwargs['pk'])
        if not self.request.user.is_authenticated:
            return redirect('cinema_detail', cinema.pk)
        else:
            if self.request.user != cinema.author:
                return redirect('cinema_detail', cinema.pk)

        return super(CinemaDelete, self).get( request, *args, **kwargs)



# Функция для страницы входа в Аккаунт
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()  # Стараемся получить пользователя по логину и паролю
            if user:
                login(request, user)
                messages.success(request, 'Вы вошли в Аккаунт')
                return redirect('index')
            else:
                messages.error(request, 'Не верный логин или пароль')
                return redirect('login')
        else:
            messages.error(request, 'Не верный логин или пароль')
            return redirect('login')

    else:
        form = LoginForm()

    context = {
        'title': 'Вход в Аккаунт',
        'form': form
    }

    return render(request, 'cinema_page/login.html', context)




# Функция для выхода из аккаунта
def user_logout(request):
    logout(request)
    messages.warning(request, 'Успешны выход из аккаунта')
    return redirect('index')




# Вьюшка для страницы регистрации
def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = Profile.objects.create(user=user)
            profile.save()
            messages.success(request, 'Регистрация прошла успешно. Авторизуйтесь')
            return redirect('login')
        else:
            for field in form.errors:
                messages.error(request, form.errors[field].as_text())
                return redirect('register')

    else:
        form = RegisterForm()

    context = {
        'title': 'Регистрация',
        'form': form
    }

    return render(request, 'cinema_page/register.html', context)




# Вьшка для поиска кинофильмов
class SearchCinema(CinemaListView):
    def get_queryset(self):
        word = self.request.GET.get('q')  # Из запроса адресной строки будим получать слово
        cinemas = Cinema.objects.filter(title__icontains=word.lower()) or Cinema.objects.filter(title__icontains=word.capitalize())
        return cinemas



# Вьюшка для сохраенния комментариев
def save_comments(request, pk):
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.cinema = Cinema.objects.get(pk=pk)
        comment.save()
        messages.success(request, 'Ваш коментарий оставлен')
        return redirect('cinema_detail', pk)


# Вьшка для страницы профиля
def profile_view(request, pk):
    profile = Profile.objects.get(user_id=pk)
    cinemas = Cinema.objects.filter(author_id=pk)  # Получим кинофильмы пользователя
    try:
        most_viewed = cinemas.order_by('-views')[:1][0]  # Получаем самый просматриваемый
        recent_cinema = cinemas.order_by('-created_at')[:1][0]  #Получаем не давно добавленный

    except:
        most_viewed = 'Нет популярных'
        recent_cinema = 'Нет новинок'


    context = {
        'title': f'Профиль: {profile.user.username}',
        'profile': profile,
        'most_viewed': most_viewed,
        'recent_cinema': recent_cinema,
        'edit_account_form': EditAccountForm(instance=request.user if request.user.is_authenticated else None),
        'edit_profile_form': EditProfileForm(instance=request.user.profile if request.user.is_authenticated else None)
    }

    return render(request, 'cinema_page/profile.html', context)



# Вьюшка для изменения данных аккаунта
def edit_account_view(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = EditAccountForm(request.POST, instance=request.user)
            if form.is_valid():
                data = form.cleaned_data  # В данную переменную получим форму в виде словаря
                user = User.objects.get(id=request.user.id)

                if user.check_password(data['old_password']):
                    if data['new_password'] == data['confirm_password']:
                        user.set_password(data['new_password'])
                        user.save()
                        update_session_auth_hash(request, user)
                        messages.success(request, 'Пароль изменён')
                        return redirect('profile', user.pk)
                    else:
                        for field in form.errors:
                            messages.error(request, form.errors[field].as_text())
                else:
                    for field in form.errors:
                        messages.error(request, form.errors[field].as_text())
                form.save()

            else:
                for field in form.errors:
                    messages.error(request, form.errors[field].as_text())

            return redirect('profile', request.user.pk)

    else:
        return redirect('login')




