from django.core.management.base import BaseCommand
from django.core.management.base import BaseCommand
from django.contrib.auth.forms import PasswordChangeForm

from manageSeaMarket.models import User
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='The username of the user')
        parser.add_argument('password', type=str, help='The new password for the user')

    def handle(self, *args, **kwargs):
        username = kwargs['username']
        password = kwargs['password']
        if kwargs['password'] or kwargs['username']:
            username = input('Username: ')
            password = input('Password: ')
        try:
            user = User.objects.get(email=username)
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully set new password for user "{username}"'))
        except User.DoesNotExist:
            raise CommandError(f'User "{username}" does not exist')
