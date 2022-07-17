from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from .forms import RegisterForm, LoginForm
from .models import *
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth import logout


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
        if search_query:
            search_word = ServerWord.objects.filter(word__iexact=search_query).first()
        else:
            search_word = None
        return render(request, 'simple_dict/search_word.html', context={'word': search_word})

    def post(self, request):
        user = request.user
        search_word = request.GET.get('search')
        word = ServerWord.objects.get(word=search_word)
        if not UserServerWord.objects.filter(word=word).filter(user=user):
            UserServerWord.objects.create(word=word, user=user)
        return redirect('search_word_url')


class LoginUser(LoginView):
    authentication_form = LoginForm
    template_name = 'simple_dict/login.html'

    def get_success_url(self):
        return reverse_lazy('search_word_url')


def logout_user(request):
    logout(request)
    return redirect('search_word_url')


class ShowUserDict(View):

    def get(self,request):
        user = request.user
        user_words = UserServerWord.objects.filter(user=user)
        return render(request, 'simple_dict/user_dict.html', context={'user_words': user_words})





