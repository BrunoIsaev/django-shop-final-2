from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Product
from .forms import ProductForm


class HomeView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'
    
    def get_queryset(self):
        return Product.objects.filter(is_published=True)


class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['success'] = False
        if self.request.method == 'POST':
            context['success'] = True
        return context


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'
    login_url = 'users:login'


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('home')
    login_url = 'users:login'
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class IsOwnerOrModeratorMixin(UserPassesTestMixin):
    """Миксин для проверки: владелец или модератор."""
    
    def test_func(self):
        product = self.get_object()
        user = self.request.user
        
        # Владелец может редактировать/удалять
        if product.owner == user:
            return True
        
        # Модератор может удалять
        if user.has_perm('catalog.delete_product'):
            return True
        
        return False


class ProductUpdateView(LoginRequiredMixin, IsOwnerOrModeratorMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    login_url = 'users:login'
    
    def get_success_url(self):
        return reverse_lazy('product_detail', kwargs={'pk': self.object.pk})


class ProductDeleteView(LoginRequiredMixin, IsOwnerOrModeratorMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('home')
    login_url = 'users:login'


class UnpublishProductView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Отмена публикации продукта (только для модераторов)."""
    model = Product
    template_name = 'catalog/product_confirm_unpublish.html'
    login_url = 'users:login'
    
    def test_func(self):
        return self.request.user.has_perm('catalog.can_unpublish_product')
    
    def form_valid(self, form):
        product = self.get_object()
        product.is_published = False
        product.save()
        messages.success(self.request, f'Публикация продукта "{product.name}" отменена.')
        return redirect('home')
