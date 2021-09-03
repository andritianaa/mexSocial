from confidentialite.models import Confidentialite
from django.forms import fields
from django.shortcuts import redirect, render, get_object_or_404
from post.forms import NewPostForm

from post.models import Post, PostContenu

def NewPost(request):
    user = request.user
    files_objs = []
    
    if request.method == "POST":
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('content')
            description = form.cleaned_data.get('description')
            
            confidentialite = form.cleaned_data.get('confidentialite')
            confidentialites = get_object_or_404(Confidentialite, id = confidentialite.id)
            
            for file in files:
                file_instance = PostContenu(file=file, user=user,confidentialite=confidentialites)
                file_instance.save(file_instance)
                
            p, created =Post.objects.get_or_create(description=description,user=user,confidentialite = confidentialites)
            p.content.set(files_objs)
            p.save()
            
            return redirect ('index')
    else:
        form = NewPostForm()
        form.fields['confidentialite'].queryset = Confidentialite.objects.filter(user=user)
        
    context = {
        'form': form,
    }
    return render(request, 'newPost.html',context)