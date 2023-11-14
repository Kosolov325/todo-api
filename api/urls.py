from django.urls import path
from api.todo import TaskListCreate, TaskDetail, TaskListView, TaskDetailView, TaskListCreateView

urlpatterns = [
    # Rest
    path('rest/tasks/', TaskListCreate.as_view(), name='task-list'),
    path('rest/tasks/<int:pk>/', TaskDetail.as_view(), name='task-detail'),

    # Templates
    path('tasks/', TaskListView.as_view(), name='tasks-view'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail-view'),
    path('create_task/', TaskListCreateView.as_view(), name='create_task'),
]