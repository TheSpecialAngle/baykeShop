import json
from django.contrib.auth.models import Permission
from django.core import management
from django.core.management.base import BaseCommand, CommandError
from django.core.management.commands import loaddata
from django.conf import settings

from baykeshop.models import BaykePermission, BaykeMenu


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('data', nargs='?', type=str)

    def handle(self, *args, **options):
        print(options)
        if options['data'] is None:
            menus_json = f"{settings.BASE_DIR}/baykeshop/config/db/baykemenu.json"
            management.call_command('loaddata', menus_json, verbosity=0)
            menus = BaykeMenu.objects.all()
            perms = Permission.objects.all()
            print(menus)
            print(perms)
            self.stdout.write(self.style.SUCCESS('Successfully "%s"' % 'push data'))