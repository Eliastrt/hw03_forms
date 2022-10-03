from django.views.generic import CreateView
from django.shortcuts import render, redirect

# Функция reverse_lazy позволяет получить URL по параметрам функции path()
from django.urls import reverse_lazy

from .forms import CreationForm, ContactForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('posts:index')
    template_name = 'users/signup.html'


def user_contact(request):
    if request.method == 'POST':

        form = ContactForm(request.POST)

        # Если все данные формы валидны - работаем с "очищенными данными" формы
        if form.is_valid():
            # Берём валидированные данные формы из словаря form.cleaned_data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['body']
            # При необходимости обрабатываем данные
            # ...
            # сохраняем объект в базу
            form.save()

            # Функция redirect перенаправляет пользователя
            # на другую страницу сайта, чтобы защититься
            # от повторного заполнения формы
            return redirect('/thank-you/')

        # Если условие if form.is_valid() ложно и данные не прошли валидацию -
        # передадим полученный объект в шаблон,
        # чтобы показать пользователю информацию об ошибке

        # Заодно заполним все поля формы данными, прошедшими валидацию,
        # чтобы не заставлять пользователя вносить их повторно
        return render(request, 'contact.html', {'form': form})

        # Если пришёл не POST-запрос - создаём и передаём в шаблон пустую форму
        # пусть пользователь напишет что-нибудь
    form = ContactForm()
    return render(request, 'contact.html', {'form': form})
