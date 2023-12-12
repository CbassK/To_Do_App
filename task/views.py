from django.shortcuts import render, reverse, redirect
from django.views import generic, View
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.db import transaction

from .models import Task
from .froms import TaskForm, TaskOrderingForm

class LandingPageView(generic.TemplateView):
    template_name = 'landing.html'


class RegisterView(generic.CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse('task:task-list')


class UserLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse('task:task-list')


class TaskListView(LoginRequiredMixin, generic.ListView):
    template_name = 'task/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        user = self.request.user
        queryset = Task.objects.filter(user=user)

        search_query = self.request.GET.get('search') or ''
        if search_query:
            queryset = queryset.filter(title__icontains=search_query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['incomplete_tasks_count'] = Task.objects.filter(user=self.request.user, complete=False).count()

        return context


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'task/task_detail.html'
    context_object_name = 'task'

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(user=user)


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'task/task_create.html'
    form_class = TaskForm

    def get_success_url(self):
        return reverse('task:task-list')


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'task/task_update.html'
    form_class = TaskForm

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(user=user)

    def get_success_url(self):
        return reverse('task:task-list')


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = 'task/task_delete.html'
    context_object_name = 'task'

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(user=user)

    def get_success_url(self):
        return reverse('task:task-list')


class TaskOrderView(LoginRequiredMixin, View):
    def post(self, request):
        form = TaskOrderingForm(request.POST)

        if form.is_valid():
            ordered = form.cleaned_data['position'].split(',')

        with transaction.atomic():
            self.request.user.set_task_order(ordered)

        return redirect('task:task-list')





