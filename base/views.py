from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login ,logout
from .models import Room,Topic,Message
from django.contrib.auth.forms import UserCreationForm
from .forms import Roomform
from django.db.models import Q
# Create your views here.
# rooms = [

#     {'id':1 , 'name':'Abhay\'s chatroom'},
#     {'id':2 , 'name':'yoshi\'s chatroom'},
#     {'id':3 , 'name':'global chatroom'},

# ]


def loginpage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request , 'user does not exist!')
        
        user = authenticate(request , username=username , password=password)
        if user is not None:
            login(request , user)
            return redirect('home')
        else:
            messages.error(request , 'Wrong password!' )
    return render(request , 'base/userlogin.html' , {'page':page})


def registerpage(request):
    form = UserCreationForm
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.username = user.username.lower()
            user.save()
            login(request , user)
            return redirect('home')
        else:
            messages.error(request , 'An error ocurred in registration!')
    return render(request , 'base/userlogin.html' , {'form':form})


def logoutview(request):
    logout(request)
    return redirect('home')


@login_required(login_url='login')
def profilepage(request, pk):
    user = User.objects.get(id = pk)
    rooms = Room.objects.filter(host = user)
    pr = Message.objects.filter(user = user)
    topics = Topic.objects.all()
    rc = rooms.count()
    context = {
        'user':user,
        'rooms':rooms,
        'pr':pr,
        'topics':topics,
        'rc':rc
    }
    return render(request , 'base/profile.html', context)

def home(request):
    q = request.GET.get('q')
    if q:
        if q == "all":
            rooms=Room.objects.all()
        else:
            rooms=Room.objects.filter(
                Q(topic__name__icontains =q) |
                Q(name__icontains = q) |
                Q(description__icontains =q )
                )
    else:
        rooms = Room.objects.all()

    rc = rooms.count()    
    topics =Topic.objects.all()
    if request.user.is_authenticated:

        prooms = Room.objects.filter(participants__in = [request.user.id] )
        msgs = Message.objects.filter(room__in = prooms ).order_by('-updated' , '-created') 
    else:
        msgs = None
    context ={
        'rooms':rooms,
        'topics':topics,
        'rc':rc,
        'pr':msgs
        } 
    return render(request , 'base/home.html' ,context)

def roomcode(request , pk):

    paswd = Room.objects.get(id = pk).password
    if request.method == 'POST':
        if request.POST.get('paswd') == paswd:     
            return redirect('room' , pk=pk)
        else:
            messages.error(request , 'Wrong code!')

    context = {

    }
    return render(request , 'base/roomcode.html' , context)

@login_required(login_url='login')
def room(request,pk):
    i = Room.objects.get(id = int(pk))
    private = i.private
    paswd = i.password 
    msgs = Message.objects.filter(room = i) 
    rooms = Room.objects.all()
    if request.method == 'POST':
        if request.POST.get('msg'):
            m = Message.objects.create(
            user=request.user,
            room = i,
            body = request.POST.get('msg')

            )
            i.participants.add(request.user)
            return redirect('room',pk = i.id)
        
        
    participants = i.participants.all()
    context = { 'room':i , 
               'rooms':rooms , 
               'msgs':msgs,
               'participants':participants,
               'private' : private,
               'paswd' : paswd

               }   
    return render(request , 'base/room.html' ,context)


@login_required(login_url='login')
def create_room(request):
    rooms = Room.objects.all()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topicname = request.POST.get('topic')
        topic , created = Topic.objects.get_or_create(name=topicname)
        room = Room.objects.create(
            host = request.user,
            topic= topic,
            name = request.POST.get('name'),
            description = request.POST.get('description'),
            private = request.POST.get('private')
        )
       
        return redirect('home')

    return render(request , 'base/room_form.html' , {'topics' : topics, 'rooms':rooms})

def update_room(request ,pk):
    rooms = Room.objects.all()
    room = Room.objects.get(id=pk)
    

    if request.method == 'POST':
        roomtopic = request.POST.get('topic')
        topic ,created = Topic.objects.get_or_create(name = roomtopic)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.private = request.POST.get('private')
        room.password = request.POST.get('password')

        room.save()
        return redirect('home')

    return render(request , 'base/room_form.html' ,{'room' : room , 'rooms':rooms})

def delete_room(request, pk):
    rooms = Room.objects.all()
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context = {'obj':room , 
               'rooms':rooms}
    return render(request , 'base/delete.html'  , context)

def delete_msg(request, pk):
    rooms = Room.objects.all()
    msg = Message.objects.get(id=int(pk))
    room = msg.room
    i = room.id
    if request.method == 'POST':
        msg.delete()
        return redirect('room' ,pk=i)
    context = {'obj':msg , 
               'rooms':rooms}
    return render(request , 'base/delete.html'  , context)

def browsetopics(request):
    topics =Topic.objects.all()
    return render(request , 'base/mobilebrowsetopics.html' ,{'topics':topics})

def activity(request):
    if request.user.is_authenticated:

        prooms = Room.objects.filter(participants__in = [request.user.id] )
        msgs = Message.objects.filter(room__in = prooms ).order_by('-updated' , '-created') 
    else:
        msgs = None
    return render(request , 'base/mobileactivity.html' ,{'pr':msgs})

def useractivity(request , pk):
    user = User.objects.get(id = pk)
    msgs = Message.objects.filter(user = user)
    context = {'pr':msgs , 'usr':user}
    return render(request, 'base/mobileactivity.html' , context)