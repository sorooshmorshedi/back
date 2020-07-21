import os
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'load fixtures'

    def handle(self, *args, **options):
        os.chdir("home/fixtures")
        fixtures = os.listdir()
        fixtures.sort()
        for fixture in fixtures:
            print(fixture)
            call_command('loaddata', fixture)
