from django.core.management.base import BaseCommand
from django.core.management.color import no_style
from django.db import connection
from django.contrib.auth import authenticate
from manageSeaMarket.models import Category, Product
import getpass

class Command(BaseCommand):
    help = 'Delete all category and product in the database'
    def handle(self, *args, **options):
        try:
            print('Connexion requise')
            email = input('Email : ')
            password = getpass.getpass('Password : ')
            user = authenticate(email=email, password=password)
            if user is None:
                self.stdout.write(self.style.ERROR('Email ou mot de passe incorrecte'))
                return 
            result = input('Êtes-vous sûr de vouloir supprimer toutes les catégories et tous les produits de la base de données ? (Defaut non)')
            if result not in ['yes', 'y']:
                self.stdout.write(self.style.ERROR('Abandon de la suppression de toutes les catégories et de tous les produits dans la base de données'))
                return
            with connection.schema_editor() as schema_editor:
                schema_editor.delete_model(Category)
                schema_editor.delete_model(Product)
                schema_editor.create_model(Category)
                schema_editor.create_model(Product)
            self.stdout.write(self.style.SUCCESS('Successfully deleted all category and product in the database'))
        except KeyboardInterrupt:
            self.stdout.write(self.style.ERROR('Abandon de la suppression de toutes les catégories et de tous les produits dans la base de données'))
    
    