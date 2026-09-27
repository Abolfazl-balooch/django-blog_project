from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Model
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView, FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from blog.models import article, Category, Comment, Message, Like
# from .forms import MessageForm, ArticleCreateForm
from django.views.generic.base import View, RedirectView
# Create your views here.

from django.urls import reverse_lazy, reverse

from django.shortcuts import get_object_or_404, redirect, render


def post_detail(request, slug):  # دریافت slug به جای pk یا id
    # پیدا کردن مقاله بر اساس slug به جای id=1
    articles = get_object_or_404(article, slug=slug)

    if request.method == 'POST':
        content = request.POST.get('message')
        if content:  # بررسی اینکه کامنت خالی نباشد
            Comment.objects.create(
                author=request.user, article=articles, content=content
            )
            # ریدایرکت به صفحه مقاله بعد از ارسال کامنت
            return redirect(articles.get_absolute_url())

    return render(request, 'blog/post_details.html', {'articles': articles})


def blog_entries(request):
    articles = article.objects.all()
    paginator = Paginator(articles, 3)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'blog/Blog Entries.html', {'all_articles': page})


def category_detail(request, pk):
    category = get_object_or_404(Category, id=pk)
    article = category.articles.all()
    return render(request, 'blog/Blog Entries.html', {'all_articles': article})


def search(request):
    query = request.GET.get('q')
    articles = article.objects.filter(title__icontains=query)
    paginator = Paginator(articles, 1)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'blog/Blog Entries.html', {'all_articles': page})


from django.shortcuts import render
from .forms import MessageForm, ArticleCreateForm


def contact_us(request):
    if request.method == 'POST':
        form = MessageForm(data=request.POST)  # تغییر نام متغیر به شکل مفرد (form)
        if form.is_valid():
            # name = form.cleaned_data['name']
            # email = form.cleaned_data['email']
            # subject = form.cleaned_data['subject']
            # message = form.cleaned_data['message']
            # Message.objects.create(name=name, email=email, subject=subject, message=message)
            instance = form.save(commit=False)
            # instance.name = request.user
            instance.save()
    else:
        form = MessageForm()  # استفاده از form مفرد
    return render(request, 'blog/contact_us.html', {'form': form})


class HomePageRedirectView(RedirectView):
    pattern_name = 'home'


permanent = False
query_string = True


def get_redirect_url(self, *args, **kwargs):
    return super().get_redirect_url(*args, kwargs)


class PostDetailView(DetailView):
    model = article
    template_name = 'blog/post_details.html'
    context_object_name = 'articles'  # A point: contex object name == model name

    # queryset = article.objects.filter(status='published')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article_object = self.object
        user = self.request.user
        if user.is_authenticated:
            context['is_liked'] = Like.objects.filter(article=article_object).exists()
        else:
            context['is_liked'] = False
        context['likes_count'] = article_object.likes.count()
        # Anything you want to send to your template extremely
        return context


class ArticleListView(ListView):
    model = article
    template_name = 'blog/Blog Entries.html'
    context_object_name = 'all_articles'  # even you can use object list in your template instate using context_object_name
    paginate_by = 2


class ContctUsView(FormView):
    form_class = MessageForm
    template_name = 'blog/contact_us.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form_data = form.cleaned_data
        Message.objects.create(**form_data)
        return super().form_valid(form)


#
class ArticleCreateView(CreateView):
    model = article
    form_class = ArticleCreateForm  # بدون پرانتز ()
    # fields = ('title', 'content', 'category' , 'image')
    template_name = 'blog/article_create.html'
    success_url = reverse_lazy('post_detail')

    def form_valid(self, form):
        form.instance.author = self.request.user.username
        return super().form_valid(form)


class ArticleUpdateView(UpdateView):
    model = article
    form_class = ArticleCreateForm
    template_name = 'blog/article_create.html'
    success_url = reverse_lazy('article_detail')

    def get_queryset(self):
        return article.objects.filter(author=self.request.user)


class ArticlePrivateListView(LoginRequiredMixin, ListView):
    model = article
    template_name = 'blog/article_list.html'
    context_object_name = 'all_articles'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_articles = article.objects.filter(author=self.request.user)
        context['user_articles'] = user_articles
        return context


class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    model = article
    success_url = reverse_lazy('post_entries')


from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View

from .models import article, Like


class LikeView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        Article = get_object_or_404(article, slug=kwargs['slug'])
        user = request.user

        like, created = Like.objects.get_or_create(article=Article, user=user)
        if not created:
            like.delete()
            liked = False
        else:
            liked = True

        return JsonResponse({
            'liked': liked,
            'likes_count': Article.likes.count()
        })