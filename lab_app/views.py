from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth import logout, login
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View, ListView, UpdateView
from django.urls import reverse
from lab_app.forms import ChangeForm
from lab_app.models import Film, Review

from django.views.decorators.csrf import csrf_exempt
import json
import math


# Список фильмов
class ListFilmView(ListView):
    model = Film
    template_name = 'film_list.html'
    context_object_name = 'films'
    paginate_by = 4

    def get(self, request, page=1):

        # Количество фильмов на странице
        elements_on_page = 6

        # Количество фильмов в строке
        elements_in_row = 3

        films = Film.objects.all()
        pages_count = math.ceil(len(films) / elements_on_page)

        start_index = (int(page) - 1) * elements_on_page
        end_index = start_index + elements_on_page
        films = films[start_index:end_index]

        index = 1
        rows = []
        row = []
        for film in films:
            row.append(film)

            if index == elements_in_row:
                rows.append(row)
                row = []
                index = 1
            else:
                index += 1

        if len(row) > 0:
            rows.append(row)

        return render(request, 'film_list.html', {"films": rows, "page": page, "pages_count": pages_count})


# Страница добавления фильма
class AddFilmView(View):

    def post(self, request):
        if request.POST:
            name = request.POST['filmName']
            description = request.POST['filmDescription']
            director = request.POST['filmDirector']
            image = request.FILES['filmImage']

            film = Film(name=name, description=description, director=director, image=image)
            film.save()
            if film is not None:
                return redirect("/")

        return redirect("/invalidFilm")


# Страница с информацией о фильме и отзывами
class FilmView(View):

    def get(self, request, film_id):

        elements_in_row = 2
        film = Film.objects.get(id=film_id)
        reviews = Review.objects.filter(film_id=film_id)
        reviews_count = len(reviews)

        index = 1
        rows = []
        row = []
        for review in reviews:
            row.append(review)

            if index == elements_in_row:
                rows.append(row)
                row = []
                index = 1
            else:
                index += 1

        if len(row) > 0:
            rows.append(row)

        if len(rows) == 0:
            rows = None

        return render(request, 'film.html', {"film": film, "reviews": rows, "reviews_count": reviews_count})


# Страница регистрации
class SignUpView(View):

    def post(self, request):
        logout(request)
        if request.POST:
            user = User.objects.create_user(
                username=request.POST['username'],
                password=request.POST['password'],
                email=request.POST['email']
            )

            if user is not None:
                login(request, user)
                return redirect("/")

        return redirect("/invalidUser")


# Страница авторизации
class LoginView(View):

    def post(self, request):
        logout(request)
        if request.POST:
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")

        return redirect("/invalidUser")


# Страница выхода
class LogoutView(View):

    def post(self, request):
        logout(request)
        return redirect("/")


class ChangeUpdateView(UpdateView):
    model = User
    template_name = 'change_form.html'
    form_class = ChangeForm
    success_url = '/change/'


# Создание и сохранение отзыва
@csrf_exempt
def create_review(request):
    if request.method == 'POST':
        review_text = request.POST.get('review_text')
        film_id = request.POST.get('film_id')

        # Создаем отзыв и сохраняем в БД
        user = User.objects.get(id=request.user.id)
        film = Film.objects.get(id=film_id)
        review = Review(description=review_text, user=user, film=film)
        review.save()

        # Формируем json с отзывом для обновления страницы
        response_data = dict()
        response_data["review_description"] = review.description
        response_data["film_id"] = review.film_id
        response_data["user_name"] = review.user.username
        response_data["reviews_count"] = int(request.POST.get('reviews_count')) + 1

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"oooops": "nothing"}),
            content_type="application/json"
        )


class AboutView(View):

    def get(self, request):

        return render(request, 'about.html')


class InfoView(View):

    def get(self, request):

        return render(request, 'page.html')


@csrf_exempt
def change_profile(request):
    args = {}

    if request.method == 'POST':
        form = ChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('change_profile'))
    else:
        form = ChangeUpdateView()

    args['form'] = form
    return render(request, 'page.html', args)