from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from wcd_mainapp.models import Tasks
from wcd_mainapp.forms import *
from wcd_mainapp.image_wcd import ImageWCD
from loguru import logger

# Create your views here.

def periodic_task_handler():
    logger.debug("periodic task handler started")
    all_tasks = Tasks.objects.all()
    for task in all_tasks:
        if task.detection_type == 1:
            try:
                ImageWCD(task.id, task.web_url, task.partOf, task.threshold).run()
                logger.success("Task-{} suceeded", task.id)
            except:
                logger.error("Task-{} failed", task.id)

def task_handler(id, url, type, threshold=1.0, css="full"):
    if type == 1:
        ImageWCD(id, url, css, threshold).run()

def home(request):
    return render(request, 'wcd_mainapp/home.html')

def all_tasks(request):
    context = {
        'tasks':Tasks.objects.all()
    }
    return render(request, 'wcd_mainapp/tasks.html', context)

def add_tasks(request):
    if request.method == 'POST':
        add_form = TasksCreateForm(request.POST or None)
        if add_form.is_valid():
            add_form.save()
            data = add_form.cleaned_data
            task_handler(data['id'], data['web_url'], 1)
            messages.success(request, f"Your Task details has been saved!")
        return redirect('all_tasks')
    else:
        add_form = TasksCreateForm()

    context = {
        'add_form': add_form,
    }

    return render(request, 'wcd_mainapp/add_tasks.html', context)
    

def update_tasks(request, id):
    if request.method == 'POST':
        instance = get_object_or_404(Tasks, id=id)
        update_form = TasksUpdateForm(request.POST, instance=instance)
        if update_form.is_valid():
            update_form.save()
            periodic_task_handler()
            return HttpResponse(status=200)
            # messages.success(request, f"Your Task details has been updated!")
        else:
            return HttpResponse(status=400)
            # messages.error(request, f"Update failed!")

    return HttpResponse(status=405)
    

def delete_tasks(request, id):
    if request.method == "DELETE":
        # if request.user:
        vehicle = get_object_or_404(Tasks, id=id)
        vehicle.delete()
        # messages.success(request, f"Deletion Successful!")
        return HttpResponse(status=200)
        # else:
            # return HttpResponse(status=403)
    else:
        return HttpResponse(status=405)
