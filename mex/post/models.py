from django import dispatch
from django.db.models.fields import related
from django.urls                import reverse
from django.db                  import models
from django.contrib.auth.models import User
from confidentialite.models     import Confidentialite, Abonnement
from django.db.models.signals   import post_save
import uuid
from django.dispatch            import receiver

def user_directory_path(instance, filename):
    #alefa any amin'ny MEDIA_ROOT / user(id)
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class PostContenu(models.Model):
    date            = models.DateTimeField(auto_now_add=True)
    file            = models.FileField(upload_to=user_directory_path)
    user            = models.ForeignKey(User, on_delete=models.CASCADE, related_name='content_owner')
    confidentialite = models.ForeignKey(Confidentialite, on_delete=models.CASCADE, related_name='tier_file')
    
class Post(models.Model):
    id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    date            = models.DateTimeField(auto_now_add=True)
    likes           = models.IntegerField(default=0)
    content         = models.ManyToManyField(PostContenu,related_name='contents')
    comments        = models.IntegerField(default=0)
    favorites       = models.IntegerField(default=0)
    description     = models.TextField(max_length=16000,verbose_name='description')
    confidentialite = models.ForeignKey(Confidentialite, on_delete=models.CASCADE, related_name='tiers')
    
    def get_absolute_url(self):
        return reverse('postdetails', args=[str(self.id)])
    
class Stream(models.Model):
    suivi    = models.ForeignKey(User,on_delete=models.CASCADE, related_name='stream_suivi')
    user     = models.ForeignKey(User,on_delete=models.CASCADE)
    post     = models.ForeignKey(Post,on_delete=models.CASCADE)
    date     = models.DateTimeField(auto_now_add=True)
    visible  = models.BooleanField(default=False)
    
    @receiver(post_save, sender=Post, dispatch_uid ='unique_add_post')
    def add_post(sender,instance, created,**kwargs):
        post = instance
        user = post.user
        if created:
            suivants = Abonnement.objects.all().filter(suivi=user)
            for suivant in suivants:
                if(suivant.confidentialite.numero >= post.confidentialite.numero):
                    stream = Stream(post= post, user= suivant.suivant, date= post.date, suivi= user, visible= True)
                    stream.save()
                else:
                    stream = Stream(post= post, user= suivant.suivant, date= post.date, suivi= user)
                    stream.save()
                    
    
class Likes(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name= 'user_likes')
    post = models.ForeignKey(Post,on_delete=models.CASCADE, related_name='post_likes')
    