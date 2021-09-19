from django import forms
from django.forms import fields, models
from confidentialite.models import Confidentialite

class nouvelleConfidentialiteForm(forms.ModelForm):
    description = forms.CharField(widget=forms.TextInput(attrs={'class' : 'zone-de-texte'}), required=True)
    can_message = forms.BooleanField(required=False)
    
    class Meta:
        model = Confidentialite
        fields = ('description', 'can_message')