from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from .models import *
from .utils import *


class CarsHome(DataMixin, ListView):
    paginate_by = 3
    model = Cars
    template_name = 'cars/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Main page')

        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Cars.objects.filter(is_published=True).select_related('cat')


"""def index(request):
    posts = Cars.objects.all()

    context = {'posts': posts,
               'menu': menu,
               'title': 'Main page',
               'cat_selected': 0,
               }
    return render(request, 'cars/index.html', context=context)"""

def about(request):
    return render(request, 'cars/about.html', {'title': 'About'})


class AddArticle(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'cars/addpage.html'
    login_url = reverse_lazy('home')
    #success_url = reverse_lazy('home')
    #raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        c_def = self.get_user_context(title='Add article')
        return dict(list(context.items()) + list(c_def.items()))


"""def add_art(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            #print(form.cleaned_data)
            try:
                form.save()
                return redirect('home')
            except:
                form.add_error(None, 'Ошибка добавления поста')
    else:
        form = AddPostForm()
    return render(request, 'cars/addpage.html', {'form': form, 'menu': menu, 'title': 'Add article'})
"""
def logout_user(request):
    logout(request)
    return redirect('login')

class ShowPost(DataMixin, DeleteView):
    model = Cars
    template_name = 'cars/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))


"""def show_post(request, post_slug):
    post = get_object_or_404(Cars, slug=post_slug)

    context = {
        'post': post,
        'menu': menu,
        'title': post.title,
        'cat_selected': post.cat_id,

    }
    return render(request, 'cars/post.html', context=context)

"""
class CarsCategory(DataMixin, ListView):
    model = Cars
    template_name = 'cars/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Cars.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Category - ' + str(c.name),
                                      cat_selected=c.pk)
        return dict(list(context.items()) + list(c_def.items()))

"""def show_category(request, cat_slug):
    cat = Category.objects.filter(slug=cat_slug)
    posts = Cars.objects.filter(cat_id=cat[0].id)

    if len(posts) == 0:
        raise Http404()

    context = {'posts': posts,
               'menu': menu,
               'title': 'Category',
               'cat_selected': cat[0].id,
               }
    return render(request, 'cars/index.html', context=context)"""


"""def about_cars(request, car_id):
    return HttpResponse(f'<h1>About cars</h1> ')

def archive(request, year):
    if int(year) > 2023:
        return redirect('home', permanent=False)

    return HttpResponse(f"<h1>Archive{year}</h1>")
"""

class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'cars/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Contact')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')



class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'cars/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Sing up')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'cars/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Log in')
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Sorry( Page NotFound</h1>')