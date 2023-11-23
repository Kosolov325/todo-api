from django.utils.decorators import method_decorator
from rest_framework_extensions.mixins import CacheResponseMixin
from django.views.decorators.cache import cache_page
from rest_framework import serializers, generics
from rest_framework.reverse import reverse
from django.views.generic import View
from django.shortcuts import render
from api.domain.task import Task
from django.conf import settings

class TaskSerializer(serializers.ModelSerializer):
    links = serializers.SerializerMethodField(read_only=True)

    def get_links(self, obj):
        request = self.context.get('request')
        task_id = obj.id
        links = [
            {
                'rel': 'self',
                'href': reverse('task-detail', kwargs={'pk': task_id}, request=request)
            }
            # Adicione outros links conforme necessário
        ]
        return links
    
    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'completed', 'due_date', 'assigned_on', 'last_update', 'links')

class TaskDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'completed', 'due_date', 'assigned_on', 'last_update')

class TaskListCreate(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskDetailSerializer

class TaskDetailView(View):
    template_name = 'task_detail.html'

    def get(self, request, id):
        return render(request, self.template_name, {'id': id, 'base_url':settings.BASE_URL})
    
class TaskListView(View):
    model = Task
    template_name = 'tasks.html'

    def get(self, request):
        return render(request, self.template_name, {'base_url':settings.BASE_URL})