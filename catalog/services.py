from django.core.cache import cache
from .models import Product


def get_products_by_category(category_id, ttl=300):
    """
    Возвращает список всех продуктов в указанной категории.
    Использует низкоуровневое кэширование с ключом category_{id} и TTL 300 секунд.
    """
    cache_key = f'category_{category_id}'

    # Пытаемся получить данные из кэша Redis
    products = cache.get(cache_key)

    if products is None:
        # Если в кэше нет — запрашиваем из базы данных
        products = list(
            Product.objects.filter(
                category_id=category_id,
                is_published=True
            ).select_related('category')
        )
        # Сохраняем результат в кэш с TTL
        cache.set(cache_key, products, timeout=ttl)

    return products
