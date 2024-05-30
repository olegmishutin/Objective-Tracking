from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import generic
from django.contrib.auth import get_user_model
from .forms import ProjectForm, TaskForm
from .models import Projects, Task


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()

        if self.request.user != project.owner:
            context['tasks'] = project.tasks.filter(executor_id=self.request.user.id)

        return context

    def get(self, request, *args, **kwargs):
        project = self.get_object()

        if project.participants.filter(id=request.user.id).exists():
            return super().get(request, *args, **kwargs)
        return HttpResponse(status=403)

    def post(self, request, *args, **kwargs):
        project = self.get_object()

        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            retProject = form.save(commit=False)

            retProject.setImage(request.FILES.get('photo'))
            retProject.save()
        else:
            messages.add_message(request, messages.INFO, form.errors)
        return self.get(request, *args, **kwargs)


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


@login_required()
def addParticipantToProject(request, pk):
    if request.method == 'POST':
        user = get_object_or_404(get_user_model(), email=request.POST.get('email'))
        project = get_object_or_404(Projects, pk=pk)

        if request.user == project.owner:
            project.participants.add(user)

            return redirect('projects:project', pk=pk)
        return HttpResponse(status=403)
    return HttpResponse(status=403)


@login_required()
def removeParticipantFromProject(request, projectPk, userPk):
    if request.method == 'POST':
        user = get_object_or_404(get_user_model(), pk=userPk)
        project = get_object_or_404(Projects, pk=projectPk)

        if request.user == project.owner:
            project.participants.remove(user)

            for task in project.tasks.filter(executor_id=user):
                task.executor = None
                task.save()

            return redirect('projects:project', pk=projectPk)
        return HttpResponse(status=403)
    return HttpResponse(status=403)


@login_required()
def createTask(request, pk):
    if request.method == 'POST':
        project = get_object_or_404(Projects, pk=pk)

        if request.user == project.owner:
            form = TaskForm(request.POST)

            if form.is_valid():
                task = form.save(commit=False)
                task.project = project

                if request.POST.get('email'):
                    executor = get_object_or_404(get_user_model(), email=request.POST.get('email'))

                    if project.participants.filter(id=executor.id).exists():
                        task.executor = executor
                task.save()
            else:
                return HttpResponse(status=400)
            return redirect('projects:project', pk=pk)
        return HttpResponse(status=403)
    return HttpResponse(status=403)


class TaskDetail(generic.DetailView):
    model = Task
    template_name = 'projects/task.html'
    context_object_name = 'task'

    def get(self, request, *args, **kwargs):
        self.projectId = kwargs.get('projectPk')
        project = get_object_or_404(Projects, pk=self.projectId)

        if project.owner == request.user:
            return super().get(request, *args, **kwargs)
        return HttpResponse(status=403)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projectId'] = self.projectId
        return context

    def post(self, request, *args, **kwargs):
        project = get_object_or_404(Projects, pk=kwargs.get('projectPk'))
        task = self.get_object()

        if request.user == project.owner:
            form = TaskForm(request.POST, instance=task)

            if form.is_valid():
                retTask = form.save(commit=False)

                if request.POST.get('email'):
                    executor = get_object_or_404(get_user_model(), email=request.POST.get('email'))

                    if project.participants.filter(id=executor.id).exists():
                        retTask.executor = executor
                else:
                    retTask.executor = None
                retTask.save(update_fields=['name', 'description', 'date_to_end', 'executor'])
            else:
                return HttpResponse(status=400)
            return redirect('projects:project', pk=project.id)
        return HttpResponse(status=403)


class TasksList(generic.ListView):
    model = Task
    template_name = 'projects/user_tasks.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return self.request.user.tasks.all()

    def post(self, request, projectId=0, *args, **kwargs):
        tasks = self.get_queryset() if not projectId else get_object_or_404(Projects, pk=projectId).tasks.filter(
            executor__id=request.user.id)

        for task in tasks:
            task.is_completed = True if request.POST.get(f'task_{task.id}_checkbox') else False
            task.save(update_fields=['is_completed'])

        return redirect(request.META.get('HTTP_REFERER'))


class DeleteTask(generic.DeleteView):
    model = Task

    def delete(self, request, *args, **kwargs):
        if request.method == 'POST' and request.user == kwargs['object'].project.owner:
            return super().delete(request, *args, **kwargs)
        return HttpResponse(status=403)

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')
