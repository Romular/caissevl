from django.contrib import admin
from caisse.models import *

# Register your models here.
admin.site.register(Categorie)
admin.site.register(Article)
admin.site.register(Commande)
admin.site.register(LigneCommande)
