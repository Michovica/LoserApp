from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm  
from .models import *
from django.contrib import messages
from datetime import datetime    
from django.contrib.auth import get_user_model

# Create your views here.
User = get_user_model()


def index(request):
    
    #check for login
    if request.user.is_authenticated == False:
        return redirect("Login")
    
    tasks = Task.objects.filter(owner=request.user)
    loserData = LoserValue.objects.filter(owner=request.user)   
    users = User.objects.all()
    if len(loserData) == 0:        
        return render(request, "metr/list.html", {"totalLoser": 100, "lastUpdated": None, "users": users, "tasks": tasks})
        
    
    totalLoser = loserData[0].value
    lastUpdated = getLastTime(request.user)    
    return render(request, "metr/list.html", {"totalLoser": totalLoser, "lastUpdated": lastUpdated, "users": users, "tasks": tasks})



def Login(request):
    
    if request.method == "POST":
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)

        
        userAuth = authenticate(request, username=username, password=password)
        if userAuth is not None:
            login(request, userAuth)
            
            return redirect('index')
        else:
            return redirect('Login')
    
    else:
        
        return render(request, 'metr/login.html')
            

def Register(request):
    
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            
            user = authenticate(request, username=username, password=password)
            login(request, user)                        
            return redirect('index')
        
        else:
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            
            errorString = ""
            
            for error in form.errors:
                errorString = errorString + error
            
            return render(request, 'metr/register.html', {'form': form})
        
    else:
        form = UserCreationForm()
                
    
    return render(request, 'metr/register.html', {'form': form})


def LogOut(request):
    logout(request)
    return redirect('Login') 


def AddTasks(request):
        
    #check for login
    if request.user.is_authenticated == False:
        return redirect("Login")
    
    
    #check if is right time
    lastTime = getLastTime(request.user)
    if lastTime == None or abs(lastTime - datetime.now().timestamp()) > 601200:
        pass
    else:
        return redirect("index")        

    
    tasks = Task.objects.filter(owner=request.user)

    if request.method != 'POST':        
        return render(request, 'metr/addTasks.html', {"tasks": tasks})
    
    else:    
        Task.objects.filter(owner=request.user).delete()    
        i = 0
        
        while str(i) in request.POST:
            taskName = request.POST.get(str(i))                    
            task = Task()
            task.name = taskName
            task.compleated = 0   
            task.owner = str(request.user)
            if "check"+str(i) not in request.POST:
                task.public = False
                
            task.save()         
            i += 1
            
        return render(request, 'metr/addTasks.html', {"tasks": tasks})


def FillResults(request):
    
    #check for login
    if request.user.is_authenticated == False:
        return redirect("Login")
    
    #check if is right time
    lastTime = getLastTime(request.user)
    if lastTime == None or abs(lastTime - datetime.now().timestamp()) > 601200:
        pass
    else:
        return redirect("index")      
    
    
    
    if request.method != "POST":        
        tasks = Task.objects.filter(owner=request.user)
        return render(request, 'metr/fillResults.html', {'tasks': tasks})
    
    else:
        tasks = Task.objects.filter(owner=request.user)
        
        for task in tasks:
            
            if request.POST.get(task.name) != "" and try_parse_int(request.POST.get(task.name)) != None:                
                task.compleated = int(request.POST.get(task.name))
                task.save()

            
            else:
                messages.success(request, "failed")
                return render(request, 'metr/fillResults.html', {'tasks': tasks})
        
        #update overal loser value
        curetLoserValue = getCurretLoserValue(request.user)
        if len(LoserValue.objects.filter(owner=str(request.user))) == 0:
            neco = LoserValue()
            neco.owner = str(request.user)
            neco.value = curetLoserValue
            neco.updatesCount = 1
            neco.save()
        else:
            loserRow = LoserValue.objects.filter(owner=str(request.user))[0]
            loserRow.value = calculateOverallLoser(curetLoserValue)
            loserRow.owner = str(request.user)
            loserRow.updatesCount = loserRow.updatesCount + 1
            loserRow.lastUpdated = datetime.now()
            loserRow.save()

        
        return redirect('fillResults')
            

def DisplayUser(request, username):
    
    LoserValue = getCurretLoserValue(username)
    tasks = Task.objects.filter(owner=username)
    tasksLen = len(tasks)
    tasks = tasks.filter(public=True)
    
    return render(request, "metr/userpage.html", {"username": username, "loserValue": LoserValue, "tasks": tasks, "tasksLen": tasksLen})
            
            
#region SecondaryMethods

def getLastTime(user):
    loserData = LoserValue.objects.filter(owner=user)
    
    if len(loserData) == 0:   
        return None
    
    return loserData[0].lastUpdated.timestamp()


def try_parse_int(text):
    try:
        return int(text)
    except:
        return None

def getCurretLoserValue(name):
    tasks = Task.objects.filter(owner=name)
    
    if len(tasks) == 0:
        return 100
    
    sum = 0
    for task in tasks:
        sum = sum + task.compleated            
        
    totalLoser = round(100 - sum/len(tasks))
    return totalLoser
    
    
def calculateOverallLoser(curretLoserValue, name):    
    loserRow = LoserValue.objects.filter(owner=name)[0]
    overall = loserRow.value
    updated = loserRow.updatesCount
    
    return ((overall * updated) + curretLoserValue) / (updated + 1)
    
    
#endregion 