from django.db import models
from django.contrib.auth.models import User

class Confidentialite(models.Model):
    numero = models.PositiveSmallIntegerField(default=0)
    Description = models.CharField(max_length=40,verbose_name='Description')
    can_message= models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tier_user')
    
    def __str__(self):
        return str(self.Description)
    
    def save(self, *args,**kwargs):
        nombre = Confidentialite.objects.filter(user=self.user).count()
        self.numero = nombre + 1
        return super().save(*args,**kwargs)
    
class Abonnement(models.Model):
    suivant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='suivant')
    suivi   = models.ForeignKey(User, on_delete=models.CASCADE, related_name='suivi')
    confidentialite = models.ForeignKey(Confidentialite,on_delete=models.CASCADE,related_name='tier')
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.suivant.username +" suit "+self.suivi.username+" en tant que "+self.confidentialite.Description