from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topic, User, Message
from .forms import RoomForm, UserForm


def login_page(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password wrong')

    context = {
        'page': page}
    return render(request, 'login_register.html', context)


def signin_page(request):
    page = 'signup'
    form = UserCreationForm()

    if request.method == 'POST':

        form = UserCreationForm(request.POST)
        if form.is_valid():
            print(111111111111111111)
            firstname = request.POST.get('firstname')
            lastname = request.POST.get('lastname')
            username = request.POST.get('username').username.lower()
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            user = User.objects.create_user(username=username, firstname=firstname, lastname=lastname,
                                            password=password)
            user.save()
            print(1222222222222222)
            login(request, user)
            return redirect('home')
    context = {
        'page': page,
        'form': form}

    return render(request, 'login_register.html', context)


@login_required(login_url='login')
def logout_page(request):
    logout(request)
    return redirect('home')


def home(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains=q) |
                                Q(name__icontains=q) |
                                Q(description__icontains=q) |
                                Q(host__username__icontains=q))

    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__name__icontains=q))

    context = {
        'rooms': rooms,
        'topics': topics,
        'room_count': room_count,
        'room_messages': room_messages}

    return render(request, 'home.html', context)


def room(request, pk):
    room_data = Room.objects.get(id=pk)
    room_messages = room_data.message_set.all()
    participants = room_data.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            body=request.POST.get('body'),
            room=room_data,
        )
        room_data.participants.add(request.user)
        return redirect('room', pk=pk)

    context = {
        'room': room_data,
        'room_messages': room_messages,
        'participants': participants}

    return render(request, 'room.html', context)


@login_required(login_url='login')
def create_room(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room_obj = form.save(commit=False)
            room_obj.host = request.user
            room_obj.save()
            room_obj.participants.add(request.user)

            return redirect('home')

    context = {
        'form': form}

    return render(request, 'room_form.html', context)


@login_required(login_url='login')
def update_room(request, pk):
    room_data = Room.objects.get(id=pk)
    form = RoomForm(instance=room_data)

    if request.user != room_data.host:
        return HttpResponse('404')

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room_data)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {
        'form': form}
    return render(request, 'room_form.html', context)


@login_required(login_url='login')
def delete_room(request, pk):
    room_obj = Room.objects.get(id=pk)

    if request.user != room_obj.host:
        return HttpResponse('404')

    if request.method == 'POST':
        room_obj.delete()
        return redirect('home')

    context = {
        'obj': room_obj}

    return render(request, 'delete.html', context)


@login_required(login_url='login')
def delete_message(request, pk):
    message_obj = Message.objects.get(id=pk)

    if request.user != message_obj.user:
        return HttpResponse('404')

    if request.method == 'POST':
        message_obj.delete()
        return redirect('room', pk=message_obj.room.id)

    context = {
        'obj': message_obj}

    return render(request, 'delete.html', context)


def user_profile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    user_messages = user.message_set.all()
    topics = Topic.objects.all()

    context = {
        'user': user,
        'rooms': rooms,
        'room_messages': user_messages,
        'topics': topics
    }

    return render(request, 'profile.html', context)


@login_required(login_url='login')
def edit_user(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
    context = {"form": form}

    return render(request, 'edit-user.html', context)


def topics_page(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''

    topics = Topic.objects.filter(name__icontains=q)

    context = {'topics': topics}

    return render(request, 'topics.html', context)


def activity_page(request):
    rooms = Room.objects.all()

    context = {'rooms': rooms}

    return render(request, 'activity.html', context)
