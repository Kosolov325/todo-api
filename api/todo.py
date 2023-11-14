from rest_framework import serializers, generics
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.views.generic import View
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
        labels = {
            'title': 'Título',
            'description': 'Descrição',
            'due_date': 'Data de Vencimento',
            'completed': 'Concluído'
        }
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'})
        }

class TaskDetailView(View):
    template_name = 'task_detail.html'

    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        form = TaskForm(instance=task)
        return render(request, self.template_name, {'task': task, 'form': form})

    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        form = TaskForm(request.POST, instance=task)
        
        if 'action' in request.POST and request.POST['action'] == 'delete':
            task.delete()
            return redirect('tasks-view')
        
        if form.is_valid():
            form.save()
            return redirect('task-detail-view', pk=pk)
        return render(request, self.template_name, {'task': task, 'form': form})
    
class TaskListView(View):
    model = Task
    template_name = 'tasks.html'

    def get_queryset(self):
        return Task.objects.all()
    
    def get_context_data(self, **kwargs):
        context = {}
        context['form'] = TaskForm()
        context['object_list'] = self.get_queryset()
        return context

    def get(self, request):
        context = self.get_context_data()
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = TaskForm(request.POST)
        if form.is_valid():
            instance = form.save()
            return redirect('task-detail-view', pk=instance.pk)
        else:
            context = self.get_context_data(form=form)
            return render(request, self.template_name, context)