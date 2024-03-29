from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from .forms import RegisterForm, UpdateUsername, UpdateEmail, ChangePasswordForm
from images.forms import CommentForm
from images.models import Image
from .decorators import unauthenticated_user


@unauthenticated_user
def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = RegisterForm()

    return render(request, 'registration/signup.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/')


@login_required(login_url='/login')
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST, request=request)
        if form.is_valid():
            newpassword = form.cleaned_data['newpassword1']
            username = request.user.username
            password = form.cleaned_data['oldpassword']

            user = authenticate(username=username, password=password)
            user.set_password(newpassword)
            user.save()
            return redirect('/')
    else:
        form = ChangePasswordForm()
    context = {'form': form}
    return render(request, 'accounts/change_password.html', context)


@login_required(login_url='/login')
def profile(request):
    user = request.user
    images = Image.objects.filter(author=request.user)
    form = CommentForm
    context = {'user': user, 'images': images, 'form': form}
    return render(request, 'accounts/profile.html', context)


@login_required(login_url='/login')
def update_username(request):
    user = request.user
    if request.method == 'POST':
        form = UpdateUsername(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('/profile')
    else:
        form = UpdateUsername()

    return render(request, 'accounts/update_username.html', {'form': form})


@login_required(login_url='/login')
def update_email(request):
    user = request.user
    if request.method == 'POST':
        form = UpdateEmail(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('/profile')
    else:
        form = UpdateEmail()

    return render(request, 'accounts/update_email.html', {'form': form})



