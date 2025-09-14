from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import Book



def setup_groups(sender, **kwargs):
    book_ct = ContentType.objects.get_for_model(Book)

    # Permissions
    can_view = Permission.objects.get(codename='can_view', content_type=book_ct)
    can_create = Permission.objects.get(codename='can_create', content_type=book_ct)
    can_edit = Permission.objects.get(codename='can_edit', content_type=book_ct)
    can_delete = Permission.objects.get(codename='can_delete', content_type=book_ct)

    # Group: Viewers
    viewers_group, _ = Group.objects.get_or_create(name='Viewers')
    viewers_group.permissions.set([can_view])

    # Group: Editors
    editors_group, _ = Group.objects.get_or_create(name='Editors')
    editors_group.permissions.set([can_view, can_create, can_edit])

    # Group: Admins
    admins_group, _ = Group.objects.get_or_create(name='Admins')
    admins_group.permissions.set([can_view, can_create, can_edit, can_delete])



class BookshelfConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bookshelf'

    def ready(self):
        post_migrate.connect(setup_groups, sender=self)
