from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('contacts/', views.ContactsView.as_view(), name='contacts'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('products/add/', views.ProductCreateView.as_view(), name='add_product'),
    path('products/<int:pk>/update/', views.ProductUpdateView.as_view(), name='update_product'),
    path('products/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='delete_product'),
    path('products/<int:pk>/unpublish/', views.UnpublishProductView.as_view(), name='unpublish_product'),
]
