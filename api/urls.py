from django.urls import path
from api.todo import TaskListCreate, TaskDetail, TaskListView, TaskDetailView

urlpatterns = [
    # Rest
    path('rest/tasks/', TaskListCreate.as_view(), name='task-list'),
    path('rest/tasks/<int:pk>/', TaskDetail.as_view(), name='task-detail'),

    # Templates
    path('tasks/', TaskListView.as_view(), name='tasks-view'),
    path('tasks/<int:id>/', TaskDetailView.as_view(), name='task-detail-view'),
]