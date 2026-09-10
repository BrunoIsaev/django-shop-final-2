from django.core.management.base import BaseCommand
from django.core.management import call_command
from catalog.models import Category, Product


class Command(BaseCommand):
    help = 'Загружает тестовые данные и удаляет существующие'

    def handle(self, *args, **options):
        # Удаляем все существующие данные
        self.stdout.write(self.style.WARNING('Удаление существующих данных...'))
        Product.objects.all().delete()
        Category.objects.all().delete()
        
        # Загружаем фикстуры
        self.stdout.write('Загрузка категорий...')
        call_command('loaddata', 'categories.json')
        
        self.stdout.write('Загрузка продуктов...')
        call_command('loaddata', 'products.json')
        
        self.stdout.write(self.style.SUCCESS('Тестовые данные успешно загружены!'))
