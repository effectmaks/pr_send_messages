from django.shortcuts import render
from .models import TaskList


def view_list(request):
   task_list = TaskList.objects.all()
   return render(request, 'viewlist/viewlist.html', {"task_list": task_list})
