from rest_framework import serializers, generics
from django.shortcuts import get_object_or_404
from django.views.generic import View
from django.shortcuts import render
from api.domain.task import Task
from django.conf import settings

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

class TaskDetailView(View):
    template_name = 'task_detail.html'

    def get(self, request, id):
        return render(request, self.template_name, {'id': id, 'base_url':settings.BASE_URL})
    
class TaskListView(View):
    model = Task
    template_name = 'tasks.html'

    def get(self, request):
        return render(request, self.template_name, {'base_url':settings.BASE_URL})