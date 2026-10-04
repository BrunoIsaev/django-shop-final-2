from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.urls import reverse_lazy
from .models import Product
from .forms import ProductForm


class HomeView(ListView):
    """Главная страница со списком товаров."""
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'


class ContactsView(TemplateView):
    """Страница контактов."""
    template_name = 'catalog/contacts.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['success'] = False
        if self.request.method == 'POST':
            context['success'] = True
        return context


class ProductDetailView(DetailView):
    """Детальная страница товара."""
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


class ProductCreateView(CreateView):
    """Создание нового товара."""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/add_product.html'
    success_url = reverse_lazy('home')
