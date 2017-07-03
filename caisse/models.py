from django.db import models
from django.utils import timezone
import json
from django.db.models import Sum


class Categorie(models.Model):

    nom = models.CharField(max_length=255)
    image = models.FileField()

    def __str__(self):
        return self.nom

    class Meta:
        ordering = ["nom"]


class Article(models.Model):

    nom = models.CharField(max_length=255)
    image = models.FileField()
    ordre = models.FloatField(default=0)
    prix_vente = models.FloatField(default=0)
    prix_achat = models.FloatField(blank=True, default=0, null=True)
    stock_initial = models.FloatField(blank=True, default=0, null=True)
    stock_actuel = models.FloatField(blank=True, default=0, null=True)
    categorie = models.ForeignKey(Categorie, related_name='articles')
    consigne = models.BooleanField(default=False)

    def __str__(self):
        return self.nom

    class Meta:
        ordering = ["ordre"]

    @property
    def nb_ventes(self):
        """
            Retourne le nombre d'articles vendus
        """
        return LigneCommande.objects.filter(article=self).filter(commande__payee=True).count()

    @property
    def revenus(self):
        return LigneCommande.objects.filter(article=self).filter(commande__payee=True).aggregate(Sum('prix_vente'))['prix_vente__sum']


class Commande(models.Model):
    montant_total_final = models.FloatField(default=0)
    payee = models.BooleanField(default=False)
    created = models.DateTimeField()
    updated = models.DateTimeField()

    def __str__(self):
        return str(self.id) + " - " + str(self.montant_total_final) + " €"

    def save(self):
        if not self.id:
            self.created = timezone.now()
        self.updated = timezone.now()
        super().save()

    def to_json(self):
        return json.dumps({
            "id": self.id,
            "montant_total_final": self.montant_total_final,
            "payee": self.payee,
            "created": self.created.isoformat(),
            "updated": self.updated.isoformat(),
        })

    def add_ligne(self, article):
        """
            Ajoute une ligne a la commande avec l'article passé en paramètre
        """
        ligne = LigneCommande(commande=self, article=article, prix_vente=article.prix_vente)
        ligne.save()
        return ligne.id

    def get_prix_total(self):
        """
            Retourne le prix total de la commande (ie somme du prix de chaque ligne)
        """
        prix_total = 0
        for line in self.lignes.all():
            prix_total = prix_total + line.prix_vente
        return prix_total


class LigneCommande(models.Model):
    commande = models.ForeignKey(Commande, related_name='lignes')
    article = models.ForeignKey(Article, related_name='lignes_commandes')
    prix_vente = models.FloatField(default=0)
    created = models.DateTimeField(default=None, null=True)
    updated = models.DateTimeField(default=None, null=True)

    def save(self):
        if not self.id:
            self.created = timezone.now()
        self.updated = timezone.now()
        super().save()
