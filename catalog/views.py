from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from .forms import ProductForm


def home(request):
    products = Product.objects.all()
    return render(request, 'catalog/home.html', {'products': products})


def contacts(request):
    success = False
    if request.method == "POST":
        success = True
    return render(request, "catalog/contacts.html", {"success": success})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'catalog/product_detail.html', {'product': product})


def add_product(request):
    """View for adding a new product via form."""
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProductForm()
    return render(request, 'catalog/add_product.html', {'form': form})
