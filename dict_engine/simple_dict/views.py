from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from .forms import RegisterForm, LoginForm, CreateUserWordForm, CreateUserWordDetailForm
from .models import *
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404
from django.forms.models import modelformset_factory


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
        if not UserWord.objects.filter(word=word.word).filter(user=user):
            user_word = UserWord.objects.create(word=word, user=user)
            UserWordDetail.objects.create(translate=word.translate, word_example=word.word_example, user_word=user_word)
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
        user_words = UserWord.objects.filter(user=user)
        user_words
        return render(request, 'simple_dict/user_dict.html', context={'user_words': user_words})


class CreateUserWord(View):

    def get(self, request):
        form_word = CreateUserWordForm()
        form_detail = CreateUserWordDetailForm()
        return render(request, 'simple_dict/create_user_word.html',
                      context={'form': form_word, 'form_detail': form_detail})

    def post(self, request):
        bounded_form = CreateUserWordForm(request.POST)
        bounded_form_detail = CreateUserWordDetailForm(request.POST)

        if bounded_form.is_valid() and bounded_form_detail.is_valid():
            parent_form = bounded_form.save(commit=False)
            parent_form.user = request.user
            parent_form.save()
            child_form = bounded_form_detail.save(commit=False)
            child_form.user_word = parent_form
            child_form.save()
            return redirect('user_dict_url')
        return render(request, 'simple_dict/create_user_word.html',
                      context={'form': bounded_form, 'form_detail': bounded_form_detail})


class ShowUserWordDetail(View):

    def get(self, request, slug):
        user_word = get_object_or_404(UserWord, slug=slug)
        return render(request, 'simple_dict/user_word_detail.html', context={'user_word': user_word})


class UpdateUserWord(View):

    def get(self, request, slug):
        user_word = UserWord.objects.get(slug=slug)
        user_word_detail = user_word.userworddetail_set.all()
        form = CreateUserWordForm(instance=user_word)
        UserWordDetailFormSet = modelformset_factory(UserWordDetail, form=CreateUserWordDetailForm, extra=0)
        form_set = UserWordDetailFormSet(queryset=user_word_detail)
        return render(request, 'simple_dict/update_user_word.html', context={'form': form, 'formset': form_set})

    def post(self, request, slug):
        user_word = UserWord.objects.get(slug=slug)
        if request.POST:
            print(request.POST)
        bounded_form = CreateUserWordForm(request.POST, instance=user_word)
        user_word_detail = user_word.userworddetail_set.all()
        UserWordDetailFormSet = modelformset_factory(UserWordDetail, form=CreateUserWordDetailForm, extra=0)
        bounded_formset = UserWordDetailFormSet(request.POST, queryset=user_word_detail)
        if bounded_form.is_valid() and bounded_formset.is_valid():
            print('save method')
            parent = bounded_form.save(commit=False)
            parent.user = request.user
            parent.save()
            for form in bounded_formset:
                child = form.save(commit=False)
                # if child.user_word is None:
                child.user_word = parent
                child.save()
            return redirect('user_dict_url')
        else:
            return render(request, 'simple_dict/update_user_word.html', context={'form': bounded_form,
                                                                                 'formset': bounded_formset})



