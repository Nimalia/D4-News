from django.contrib.auth.mixins import PermissionRequiredMixin

from datetime import datetime
from django.urls import reverse_lazy

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Author
from .filters import PostFilter
from .forms import PostForm
from django.core.exceptions import PermissionDenied



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
