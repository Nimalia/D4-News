from django.contrib.auth.mixins import PermissionRequiredMixin

from datetime import datetime
from django.urls import reverse_lazy

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .filters import PostFilter
from .forms import PostForm
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Category, Post


class PostList(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'flatpages/news.html'
    context_object_name = 'news'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next post'] = None
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'flatpages/new.html'
    context_object_name = "new"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context


class PostSearchList(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'flatpages/search.html'
    context_object_name = 'search'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next post'] = None
        context['filterset'] = self.filterset
        return context


class PostSearchDetail(DetailView):
    model = Post
    template_name = 'flatpages/search.html'
    context_object_name = "search"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ("newsandart.add_post",)
    # raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'flatpages/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user.author
        return super().form_valid(form)
    # def form_valid(self, form):
    #     fields = form.save(commit=False)
    #     fields.postAuthor = Author.objects.get(author_user=self.request.user)
    #     fields.save()
    #     return super().form_valid(form)


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ("newsandart.add_post",)
    form_class = PostForm
    model = Post
    template_name = 'flatpages/edit.html'

    def has_permission(self):
        perms = self.get_permission_required()
        if not self.get_object().author.authorUser == self.request.user:
            raise PermissionDenied()
        return self.request.user.has_perms(perms)


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ("newsandart.add_post",)
    model = Post
    template_name = 'flatpages/delete.html'
    success_url = reverse_lazy('post_list')


class CategoryListView(ListView):
    model = Post
    template_name = "flatpages/category_list.html"
    context_object_name = "category_news_list"

    def get_queryset(self):
        self.postCategory = get_object_or_404(Category, id=self.kwargs["pk"])
        queryset = Post.objects.filter(postCategory=self.postCategory).order_by("-dateCreation")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_not_subscriber"] = self.request.user not in self.postCategory.subscribers.all()
        context["category"] = self.postCategory
        return context


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = "Вы успешно подписались на рассылку новостей данной категории"
    return render(request, "flatpages/subscribe.html", {"category": category, "message": message})

@login_required
def unsubscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.remove(user)

    message = "Вы успешно  отписались от рассылки новостей данной категории"
    return render(request, "flatpages/unsubscribe.html", {"category": category, "message": message})