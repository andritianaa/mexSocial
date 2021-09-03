from authy.models import Profile
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls.conf import include
from confidentialite.views import Subscribe

from authy.views import UserProfile

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/',include('authy.urls')),
    path('sub/',include('confidentialite.urls')),
    path('post/',include('post.urls')),
    path('<username>/',UserProfile, name='profile'),
    path('<username>/<confidentialite_id>/subscribe',Subscribe, name='subscribe'),
]+ static(settings.MEDIA_URL, document_root =settings.MEDIA_ROOT)
