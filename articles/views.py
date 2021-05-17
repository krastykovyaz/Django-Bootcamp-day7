from django.shortcuts import render, redirect, reverse
from django.views.generic.base import RedirectView, TemplateView
from django.views.generic.edit import FormView
from articles.models import Article, LoginForm, UserFavouriteArticle, UserRegisterForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.views.generic import DetailView
from django.contrib import messages



# Create your views here.
class Home(RedirectView):
    pattern_name = 'articles'


class Articles(TemplateView):
    template_name = 'articles/articles.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_articles'] = Article.objects.all()
        return context


class LoginPage(FormView):
    template_name = 'articles/login.html'
    form_class = LoginForm
    success_url = 'home'
    initial = {'key': 'value'}

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            password = form.cleaned_data.get("password")
            user = authenticate(username=name, password=password)
            if user is not None:
                login(request, user=user)
                return HttpResponseRedirect(reverse('home'))
        return render(request, self.template_name, {'form': form})


class Publications(TemplateView):
    template_name = 'articles/publications.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.request.user)
        if self.request.user.is_authenticated:
            context['latest_articles'] = Article.objects.filter(author=self.request.user)
            print(context['latest_articles']['created'])
            return context
        else:
            context['latest_articles'] = 0
            return context

def register(request):
    if request.method == 'POST': # come request
        form = UserRegisterForm(request.POST) # to fill the form
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'articles/register.html', {'form': form})

class Detail(DetailView):
    model = Article


class Logout(RedirectView):
    template_name = 'articles/articles.html'

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('home'))


class Favourites(TemplateView):
    template_name = 'articles/favourites.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['latest_articles'] = UserFavouriteArticle.objects.filter(user=self.request.user)
            return context
        else:
            context['latest_articles'] = 0
            return context


