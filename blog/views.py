from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post
from .forms import PostForm


class PostListView(ListView):
    """Список опубликованных блоговых записей."""
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    
    def get_queryset(self):
        """Выводим только опубликованные записи."""
        return Post.objects.filter(is_published=True)


class PostDetailView(DetailView):
    """Детальная страница блоговой записи."""
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    
    def get_object(self, queryset=None):
        """Увеличиваем счетчик просмотров при открытии статьи."""
        obj = super().get_object(queryset)
        obj.views_count += 1
        obj.save(update_fields=['views_count'])
        return obj


class PostCreateView(CreateView):
    """Создание новой блоговой записи."""
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:post_list')


class PostUpdateView(UpdateView):
    """Редактирование блоговой записи."""
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def get_success_url(self):
        """Перенаправление на страницу отредактированной статьи."""
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.pk})


class PostDeleteView(DeleteView):
    """Удаление блоговой записи."""
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')
