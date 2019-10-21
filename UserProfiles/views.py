from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from PIL import Image
from django.db import transaction

from .forms import UserRegisterForm, ProfileRegisterForm, UserUpdateForm, PostRegUpdateForm

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileRegisterForm(request.POST,
                                request.FILES,
                                instance=request.user.profile)
        k_form = PostRegUpdateForm(request.POST,
                                request.FILES,
                                instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            k_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileRegisterForm(instance=request.user.profile)
        k_form = PostRegUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'k_form': k_form,
    }

    return render(request, 'UserProfiles/profile.html', context)




@transaction.atomic
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        profile_form = ProfileRegisterForm(request.POST, request.FILES,)

        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            user.refresh_from_db()
            profile_form =ProfileRegisterForm(request.POST, instance=user.profile)
            profile_form.full_clean()
            profile_form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('profile')
    else:
        form = UserRegisterForm()
        profile_form = ProfileRegisterForm()
    
    context = {
        'form' : form, 
        'profile_form' : profile_form
        }
    return render(request, 'UserProfiles/register.html', context)



