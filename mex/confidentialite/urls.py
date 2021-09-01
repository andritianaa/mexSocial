from django.urls import path
from confidentialite.views import nouvelleConfidentialite
urlpatterns = [
    path ('newConf/', nouvelleConfidentialite, name = 'newtier'),
]