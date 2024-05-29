from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import generic
from .forms import ProjectForm
from .models import Projects


class ProjectList(generic.ListView):
    model = Projects
    template_name = 'index.html'
    context_object_name = 'projects'

    def get_queryset(self):
        return self.request.user.projects.all()


class ProjectDetail(generic.DetailView):
    model = Projects
    template_name = 'projects/project.html'
    context_object_name = 'project'

    def get(self, request, *args, **kwargs):
        project = self.get_object()

        if project.participants.filter(id=request.user.id).exists():
            return super().get(request, *args, **kwargs)
        return HttpResponse(status=403)


@login_required()
def createProject(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)

        if form.is_valid():
            project = form.save(commit=False)

            project.setImage(request.FILES.get('photo'))
            project.owner = request.user
            project.save()

            project.participants.add(request.user)
            return redirect('projects:index')
        else:
            messages.add_message(request, messages.INFO, form.errors)
    return render(request, 'projects/create_project.html')


class DeleteProject(generic.DeleteView):
    model = Projects
    success_url = reverse_lazy('projects:index')

    def delete(self, request, *args, **kwargs):
        if request.method == 'POST' and request.user == kwargs['object'].owner:
            return super().delete(request, *args, **kwargs)
        return HttpResponse(status=403)
