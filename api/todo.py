from django.views.generic import ListView, CreateView, View
from rest_framework import serializers, generics
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from api.domain.task import Task
from django import forms


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'completed', 'due_date', 'assigned_on', 'last_update')
    
class TaskListCreate(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'completed']

class TaskDetailView(View):
    template_name = 'task_detail.html'

    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        form = TaskForm(instance=task)
        return render(request, self.template_name, {'task': task, 'form': form})

    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task-detail-view', pk=pk)
        return render(request, self.template_name, {'task': task, 'form': form})
    
class TaskListView(ListView):
    model = Task
    template_name = 'tasks.html'

    def get_queryset(self):
        return Task.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TaskForm()  
        return context

class TaskListCreateView(CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('tasks') 