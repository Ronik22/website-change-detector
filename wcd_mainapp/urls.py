from django.urls import path
from .views import home, all_tasks, add_tasks, update_tasks, delete_tasks

urlpatterns = [
    path('', home, name='home'),
    path('tasks/', all_tasks, name='all_tasks'),
    path('tasks/add/', add_tasks, name='add_tasks'),
    path('tasks/<int:id>/update/', update_tasks, name='update_tasks'),
    path('tasks/<int:id>/delete/', delete_tasks, name='delete_tasks'),
]