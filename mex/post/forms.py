from django import forms

from django.forms import fields
from post.models import Post
from confidentialite.models import Confidentialite

class NewPostForm(forms.ModelForm):
    content = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple' : True}), required=True)
    description = forms.CharField(widget=forms.Textarea(attrs={'class' : 'materialize-textarea'}), required=True)
    confidentialite = forms.ModelChoiceField(queryset=Confidentialite.objects.all())
    
    class Meta:
        model= Post
        fields = ('content','description','confidentialite')