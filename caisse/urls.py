from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^$', index_caisse, name='caisse_index'),
    url(r'ajax_nouvelle_commande/$', ajax_nouvelle_commande, name='ajax_nouvelle_commande'),
    url(r'stats/$', stats, name='statistiques'),
    url(r'ajax_add_article_commande/$', ajax_add_article_commande, name='ajax_add_article_commande'),
    url(r'ajax_remove_article_commande/$', ajax_remove_article_commande, name='ajax_remove_article_commande'),



    # url(r'^session/$', session_production, name='production_session'),
]
