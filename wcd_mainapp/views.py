from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from wcd_mainapp.models import Tasks
from wcd_mainapp.forms import *
from wcd_mainapp.image_wcd import ImageWCD
# from loguru import logger
from wcd_mainapp.tasks import periodic_task_scheduler, task_scheduler

# Create your views here.


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
            form_saved = add_form.save()
            print(add_form.cleaned_data)
            data = add_form.cleaned_data
            task_scheduler.delay(form_saved.pk, data['web_url'], 1, 1.0, "full")    # for celery task (demo data for now)
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
            periodic_task_scheduler.delay() # for celery beat (scheduled task)
            return HttpResponse(status=200)
            # messages.success(request, f"Your Task details has been updated!")
        else:
            return HttpResponse(status=400)
            # messages.error(request, f"Update failed!")

    return HttpResponse(status=405)
    

def delete_tasks(request, id):
    if request.method == "DELETE":
        # if request.user:
        task = get_object_or_404(Tasks, id=id)
        task.delete()
        # messages.success(request, f"Deletion Successful!")
        return HttpResponse(status=200)
        # else:
            # return HttpResponse(status=403)
    else:
        return HttpResponse(status=405)
