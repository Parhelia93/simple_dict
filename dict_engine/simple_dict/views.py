from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from .forms import RegisterForm, LoginForm
from .models import *
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth import logout


def index(request):
    return render(request, 'simple_dict/base_screen.html')


class RegisterUser(View):

    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'simple_dict/register_form.html', context={'register_form': register_form})

    def post(self, request):
        bound_form = RegisterForm(request.POST)
        if bound_form.is_valid():
            bound_form.save()
            return redirect(reverse('search_word_url'))
        else:
            return render(request, 'simple_dict/register_form.html', context={'register_form': bound_form})


class SearchWord(View):

    def get(self, request):
        search_query = request.GET.get('search', '')
        search_word = None
        if search_query:
            try:
                search_word = ServerWord.objects.get(word__iexact=search_query)
            except:
                search_word = None
        return render(request, 'simple_dict/search_word.html', context={'word': search_word})


class LoginUser(LoginView):
    authentication_form = LoginForm
    template_name = 'simple_dict/login.html'

    def get_success_url(self):
        return reverse_lazy('search_word_url')


def logout_user(request):
    logout(request)
    return redirect('search_word_url')




