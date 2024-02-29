from django.core.management.base import BaseCommand
import sys

class Command(BaseCommand):
    help = 'This is my custom management command'

    def handle(self, *args, **options):
        self.stdout.write('This is my custom management command output')


class Command(BaseCommand):
    def handle(self, *args, **options):
        venv_lib_root = sys.prefix + '/lib/python3.8'  # Adjust the Python version as needed
        print(venv_lib_root)