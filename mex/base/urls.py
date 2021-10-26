from django.urls import path
from django.views.generic.edit import DeleteView
from .views import TaskList, TaskDetail, TaskCreate, TaskUpdate, DeleteView, GrubView

urlpatterns = [
    path('',TaskList.as_view(), name='tasks'),
    path('grub/',GrubView.as_view(), name='grub'),
    path('task/<int:pk>/',TaskDetail.as_view(), name='task'),
    path('task-create/',TaskCreate.as_view(), name='task-create'),
    path('task-update/<int:pk>/',TaskUpdate.as_view(), name='task-update'),
    path('task-delete/<int:pk>/',DeleteView.as_view(), name='task-delete'),
]