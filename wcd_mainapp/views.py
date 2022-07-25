from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from wcd_mainapp.models import Tasks
from wcd_mainapp.forms import *
from django.contrib.auth.decorators import login_required
from wcd_mainapp.tasks import task_scheduler
from wcd_mainapp.utils import res_cleanup
from django.db import IntegrityError

# Create your views here.


def home(request):
    return render(request, 'wcd_mainapp/home.html')

@login_required
def all_tasks(request):
    context = {
        'tasks':Tasks.objects.filter(user = request.user)
    }
    return render(request, 'wcd_mainapp/tasks.html', context)

@login_required
def add_tasks(request):
    if request.method == 'POST':
        add_form = TasksCreateForm(request.POST or None)
        if add_form.is_valid():
            add_form.instance.user = request.user
            # each task must contain an unique url [for every user]
            try:
                form_saved = add_form.save()
            except IntegrityError as e: 
                if 'UNIQUE constraint failed' in e.args[0]:
                    messages.error(request, "You already have a task with the same url")
                    return redirect('add_tasks')
            data = add_form.cleaned_data
            # run for the first time with new data
            task_scheduler.delay(request.user.email, form_saved.pk, data['web_url'], data['detection_type'], data['threshold'], data['partOf'])    # for celery task
            messages.success(request, "Your Task details has been saved!")
        return redirect('all_tasks')
    else:
        add_form = TasksCreateForm()

    context = {
        'add_form': add_form,
    }

    return render(request, 'wcd_mainapp/add_tasks.html', context)
    

@login_required
def update_tasks(request, id):
    if request.method == 'POST':
        instance = get_object_or_404(Tasks, id=id)
        old_detection_type = instance.detection_type

        if not request.user == instance.user:
            return HttpResponse(status=403)

        update_form = TasksUpdateForm(request.POST, instance=instance)
        if update_form.is_valid():
            res_cleanup(id, old_detection_type)   # to cleanup leftover files
            update_form.save()
            data = update_form.cleaned_data
            # run for the first time with new data
            task_scheduler.delay(request.user.email, id, data['web_url'], data['detection_type'], data['threshold'], data['partOf'])    # for celery task
            messages.success(request, f"Your Task details has been updated!")
            return HttpResponse(status=200)
            
        else:
            messages.error(request, f"Update failed!")
            return HttpResponse(status=400)
            
    return HttpResponse(status=405)
    

@login_required
def delete_tasks(request, id):
    if request.method == "DELETE":
        task = get_object_or_404(Tasks, id=id)
        if not request.user == task.user:
            return HttpResponse(status=403)
        res_cleanup(id, task.detection_type)   # to cleanup leftover files
        task.delete()
        messages.success(request, f"Deletion Successful!")
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=405)



