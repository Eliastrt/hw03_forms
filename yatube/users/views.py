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
        if form.is_valid():

            form.save()

            return redirect('/thank-you/')

        return render(request, 'contact.html', {'form': form})

    form = ContactForm()

    return render(request, 'contact.html', {'form': form})
