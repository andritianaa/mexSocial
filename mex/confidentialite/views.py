from django.contrib.auth.models import User
from confidentialite.models import Confidentialite
from django.shortcuts import get_object_or_404, redirect, render
from confidentialite.forms import nouvelleConfidentialiteForm
from confidentialite.models import Confidentialite,Abonnement
from cryptography.fernet import Fernet

def nouvelleConfidentialite(request):
    user = request.user
    if request.method == "POST":
        form = nouvelleConfidentialiteForm(request.POST)
        if form.is_valid():
            description = form.cleaned_data.get('description')
            key = Fernet.generate_key()
            fernet= Fernet(key)
            description = fernet.encrypt(description.encode())
            
            
            can_message = form.cleaned_data.get('can_message')
            Confidentialite.objects.create(description=description, user=user, can_message=can_message)
            return redirect('index')
    else:
        form = nouvelleConfidentialiteForm()
    
    context = {
        'form' : form,
        
    }
    return render (request, 'newTier.html',context)


def Subscribe(request,username,confidentialite_id):
    user = request.user
    subscribing = get_object_or_404(User, username=username)
    confidentialite = Confidentialite.objects.get(id=confidentialite_id)
    
    try:
        Abonnement.objects.get_or_create(suivant= user,suivi=subscribing, confidentialite = confidentialite)
        return ('index')
    except User.DoesNotExist:
        return('index')