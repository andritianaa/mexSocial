from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy
from base.models import Task
from .models import Task

class GrubView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'base/grub.html'
    context_object_name = 'task'

class TaskList(LoginRequiredMixin ,ListView):
    model = Task
    context_object_name = 'tasks'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
        
        search_input = self.request.GET.get('search_area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__startswith=search_input)
            
        context['search_input'] = search_input   
        return context
        
        
class TaskDetail(LoginRequiredMixin ,DetailView):
    model = Task    
    context_object_name = 'task'
    template_name = 'base/task.html'

class TaskCreate(LoginRequiredMixin ,CreateView):
    model = Task
    fields = ['title','description','complete']
    success_url = reverse_lazy('tasks')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)    
    
    
class TaskUpdate(LoginRequiredMixin ,UpdateView):
    model = Task
    fields = ['title','description','complete']
    success_url = reverse_lazy('tasks')
    
class DeleteView(LoginRequiredMixin ,DeleteView):
    model = Task
    context_object_name = 'task'    
    success_url = reverse_lazy('tasks')