from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'projects'
urlpatterns = [
    path('', login_required(views.ProjectList.as_view()), name='index'),
    path('create-project/', views.createProject, name='create-project'),
    path('delete/<int:pk>/project/', login_required(views.DeleteProject.as_view()), name='delete-project'),
    path('project/<int:pk>/', login_required(views.ProjectDetail.as_view()), name='project')
]
