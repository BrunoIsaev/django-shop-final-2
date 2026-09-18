from django.core.management.base import BaseCommand
from catalog.models import Category, Product


class Command(BaseCommand):
    help = 'Загрузка данных о категориях и продуктах'

    def handle(self, *args, **kwargs):
        # Удаляем все существующие данные
        self.stdout.write('Удаление старых данных...')
        Product.objects.all().delete()
        Category.objects.all().delete()
        
        # Создаём категории
        self.stdout.write('Создание категорий...')
        category1 = Category.objects.create(
            name='Электроника',
            description='Электронные устройства'
        )
        category2 = Category.objects.create(
            name='Одежда',
            description='Одежда и аксессуары'
        )
        
        # Создаём продукты
        self.stdout.write('Создание продуктов...')
        Product.objects.create(
            name='Смартфон',
            description='Современный смартфон',
            price=45000,
            category=category1
        )
        Product.objects.create(
            name='Футболка',
            description='Хлопковая футболка',
            price=1500,
            category=category2
        )
        
        self.stdout.write(self.style.SUCCESS('Данные успешно загружены!'))
