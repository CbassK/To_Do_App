from django.urls import path
from .views import (TaskListView,
                    TaskDetailView,
                    TaskCreateView,
                    TaskUpdateView,
                    TaskDeleteView,
                    TaskOrderView
                    )

app_name = 'task'

urlpatterns = [
    path('', TaskListView.as_view(), name='task-list'),
    path('<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('<int:pk>/update', TaskUpdateView.as_view(), name='task-update'),
    path('<int:pk>/delete', TaskDeleteView.as_view(), name='task-delete'),
    path('create/', TaskCreateView.as_view(), name='task-create'),
    path('task_order/', TaskOrderView.as_view(), name='task-order')
]
