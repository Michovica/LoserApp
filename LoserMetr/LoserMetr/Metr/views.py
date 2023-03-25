from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages

# Create your views here.
def index(request):
    loserData = LoserValue.objects.all()   
    if len(loserData) == 0:        
        return render(request, "metr/list.html", {"totalLoser": 100})
        
    
    totalLoser = 100 - loserData[0].value
    return render(request, "metr/list.html", {"totalLoser": totalLoser})


def AddTasks(request):
    
    if request.method != 'POST':        
        return render(request, 'metr/addTasks.html')
    
    else:    
        Task.objects.all().delete()    
        i = 0
        
        while str(i) in request.POST:
            taskName = request.POST.get(str(i))                    
            task = Task()
            task.name = taskName
            task.compleated = 0   
            task.save()         
            i += 1
            
        return render(request, 'metr/addTasks.html')


def FillResults(request):
    
    if request.method != "POST":        
        tasks = Task.objects.all()
        return render(request, 'metr/fillResults.html', {'tasks': tasks})
    
    else:
        tasks = Task.objects.all()
        
        for task in tasks:
            
            if request.POST.get(task.name) != "" and try_parse_int(request.POST.get(task.name)) != None:                
                task.compleated = int(request.POST.get(task.name))
                task.save()

            
            else:
                messages.success(request, "failed")
                return render(request, 'metr/fillResults.html', {'tasks': tasks})
        
        #update overal loser value
        curetLoserValue = getCurretLoserValue()
        if len(LoserValue.objects.all()) == 0:
            neco = LoserValue()
            neco.value = curetLoserValue
            neco.updatesCount = 1
            neco.save()
        else:
            loserRow = LoserValue.objects.all()[0]
            loserRow.value = calculateOverallLoser(curetLoserValue)
            loserRow.updatesCount = loserRow.updatesCount + 1
            loserRow.save()

        
        return redirect('fillResults')
            
            
            
#region SecondaryMethods

def try_parse_int(text):
    try:
        return int(text)
    except:
        return None

def getCurretLoserValue():
    tasks = Task.objects.all()
    sum = 0
    for task in tasks:
        sum = sum + task.compleated            
        
    totalLoser = round(100 - sum/len(tasks))
    return totalLoser
    
def calculateOverallLoser(curretLoserValue):    
    loserRow = LoserValue.objects.all()[0]
    overall = loserRow.value
    updated = loserRow.updatesCount
    
    return ((overall * updated) + curretLoserValue) / (updated + 1)

    
    
    
#endregion 