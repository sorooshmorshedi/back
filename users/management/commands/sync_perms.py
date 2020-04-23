from django.core.management.base import BaseCommand
from django.contrib.auth.management import create_permissions
from django.template.backends import django


class Command(BaseCommand):
    args = '<app app ...>'
    help = 'reloads permissions for specified apps, or all apps if no args are specified'

    def handle(self, *args, **options):
        apps = []
        for model in django.apps.get_models():
            apps.append(django.apps.get_app_config(model._meta.app_label))
        for app in apps:
            create_permissions(app, 0)
