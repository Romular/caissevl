from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Categorie, Commande, Article, LigneCommande
import json
from django.db.models import Sum


def index_caisse(request):
    template = loader.get_template('index_caisse.html')
    categorie_list = Categorie.objects.all().order_by("nom")
    article_list = Article.objects.all()
    context = {
        "categorie_list": categorie_list,
        "article_list": article_list,
    }
    return HttpResponse(template.render(context, request))


def ajax_nouvelle_commande(request):
    """
        Crée une nouvelle commande. Retourne sa représentation en json :
    """
    id_commande_precedente = request.GET.get("id_paye", None)
    if id_commande_precedente is not None:
        commande_precedente = Commande.objects.get(id=id_commande_precedente)
        commande_precedente.payee = True
        commande_precedente.montant_total_final = commande_precedente.get_prix_total()
        commande_precedente.save()
    commande = Commande()
    commande.save()
    print(commande.to_json())
    return HttpResponse(commande.to_json(), content_type='application/json')


def ajax_add_article_commande(request):
    id_commande = request.GET["id_commande"]
    id_article = request.GET["id_article"]
    commande = Commande.objects.get(id=id_commande)
    article = Article.objects.get(id=id_article)
    ligne_id = commande.add_ligne(article)
    prix_total = commande.get_prix_total()
    ret = {
        "prix_total": prix_total,
        "ligne_id": ligne_id,
        "ligne_article": article.nom,
    }
    return HttpResponse(json.dumps(ret), content_type='application/json')


def ajax_remove_article_commande(request):
    id_line_commande = request.GET["id_line_commande"]
    line_commande = LigneCommande.objects.get(id=id_line_commande)
    commande = line_commande.commande
    line_commande.delete()
    ret = {
        "prix_total": commande.get_prix_total(),
    }
    return HttpResponse(json.dumps(ret), content_type='application/json')


def stats(request):
    template = loader.get_template('stats.html')
    article_list = Article.objects.all()
    ca_total = LigneCommande.objects.filter(commande__payee=True).aggregate(Sum('prix_vente'))['prix_vente__sum']
    context = {
        "article_list": article_list,
        "ca_total": ca_total,
    }
    return HttpResponse(template.render(context, request))
