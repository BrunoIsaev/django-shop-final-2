from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product


class Command(BaseCommand):
    help = 'Создает группы Модератор продуктов и Контент-менеджер с необходимыми правами'

    def handle(self, *args, **kwargs):
        # Получаем content type для Product
        product_ct = ContentType.objects.get_for_model(Product)
        
        # Получаем кастомное право can_unpublish_product
        can_unpublish_perm = Permission.objects.get(
            codename='can_unpublish_product',
            content_type=product_ct
        )
        
        # Получаем право на удаление продукта
        delete_product_perm = Permission.objects.get(
            codename='delete_product',
            content_type=product_ct
        )
        
        # Создаем группу "Модератор продуктов"
        moderator_group, created = Group.objects.get_or_create(name='Модератор продуктов')
        if created:
            moderator_group.permissions.add(can_unpublish_perm, delete_product_perm)
            self.stdout.write(self.style.SUCCESS('Группа "Модератор продуктов" создана'))
        else:
            moderator_group.permissions.add(can_unpublish_perm, delete_product_perm)
            self.stdout.write(self.style.SUCCESS('Группа "Модератор продуктов" обновлена'))
        
        # Создаем группу "Контент-менеджер" (для блога)
        from blog.models import Post
        post_ct = ContentType.objects.get_for_model(Post)
        
        # Права для блога
        add_post_perm = Permission.objects.get(codename='add_post', content_type=post_ct)
        change_post_perm = Permission.objects.get(codename='change_post', content_type=post_ct)
        delete_post_perm = Permission.objects.get(codename='delete_post', content_type=post_ct)
        
        content_manager_group, created = Group.objects.get_or_create(name='Контент-менеджер')
        if created:
            content_manager_group.permissions.add(add_post_perm, change_post_perm, delete_post_perm)
            self.stdout.write(self.style.SUCCESS('Группа "Контент-менеджер" создана'))
        else:
            content_manager_group.permissions.add(add_post_perm, change_post_perm, delete_post_perm)
            self.stdout.write(self.style.SUCCESS('Группа "Контент-менеджер" обновлена'))
        
        self.stdout.write(self.style.SUCCESS('Все группы созданы/обновлены'))
