from authy.models import Profile
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls.conf import include

from authy.views import UserProfile

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/',include('authy.urls')),
    path('<username>/',UserProfile, name='profile'),
]+ static(settings.MEDIA_URL, document_root =settings.MEDIA_ROOT)
