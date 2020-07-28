from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView
from .forms import BlogModelForm
from .models import Blog


@method_decorator(login_required(login_url='login/'), name='dispatch')
class CreateBlogView(SuccessMessageMixin, CreateView):
    form_class = BlogModelForm
    success_url = reverse_lazy('blog:list')
    model = Blog
    template_name = 'blog/create.html'
    success_message = 'Article created'

    def form_valid(self, form):
        blog = form.save(commit=False)
        blog.user = self.request.user
        blog.save()
        return super().form_valid(form)


@method_decorator(login_required(login_url='login/'), name='dispatch')
class ListBlogView(ListView):
    queryset = Blog.objects.all().order_by('-id')
    template_name = 'blog/list.html'
    context_object_name = 'blog'


@method_decorator(login_required(login_url='login/'), name='dispatch')
class DetailBlogView(DetailView):
    model = Blog
    template_name = 'blog/detail.html'
    context_object_name = 'article'


@method_decorator(login_required(login_url='login/'), name='dispatch')
class UpdateBlogView(SuccessMessageMixin, UpdateView):
    model = Blog
    form_class = BlogModelForm
    template_name = 'blog/update.html'
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('blog:list')
    success_message = 'Article updated'

    def get_queryset(self):
        return Blog.objects.filter(user=self.request.user)

    def form_valid(self, form):
        blog = form.save(commit=False)
        blog.user = self.request.user
        blog.save()
        return super().form_valid(form)


@method_decorator(login_required(login_url='login/'), name='dispatch')
class DeleteBlogView(SuccessMessageMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:list')
    success_message = 'Article deleted'

    def get_queryset(self):
        return Blog.objects.filter(user=self.request.user)

