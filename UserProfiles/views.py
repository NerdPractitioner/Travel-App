import os as os
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from PIL import Image
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from django.forms import modelformset_factory

from .models import Images
from .forms import UserRegisterForm, ProfileRegisterForm, UserUpdateForm, PostRegUpdateForm, ImageForm

@login_required
def profile(request):
    ImageFormSet = modelformset_factory(Images, form=ImageForm)

    #UserFormSet = modelformset_factory(Profile, form=ImageForm, extr=6)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileRegisterForm(request.POST,
                                request.FILES,
                                instance=request.user.profile)
        k_form = PostRegUpdateForm(request.POST,
                                request.FILES,
                                instance=request.user.profile)
        formset = ImageFormSet(request.POST, request.FILES)
        
        if u_form.is_valid()  and k_form.is_valid() and formset.is_valid():
            u_form.save()
            p_form.save()
            k_form.save()
            
            #profile_form =PostRegUpdateForm(request.POST, instance=request.user.profile)
            for form in formset.cleaned_data:
                #this helps to not crash if the user   
                #do not upload all the photos
                if form:
                    image = form['image']
                    photo = Images(profile=request.user.profile, image=image)
                    photo.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileRegisterForm(instance=request.user.profile)
        k_form = PostRegUpdateForm(instance=request.user.profile)
        formset = ImageFormSet(queryset=Images.objects.none())
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'k_form': k_form,
        'formset': formset,
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


def index(request):
    path = settings.MEDIA_ROOT
    img_list = os.listdir(path + '/images')
    context = {'images' : img_list}
    return render(request, "photo/index.html", context)
"""
@csrf_exempt
def uploadImages(request):
    try:
        if request.session['member_id'] is not None:
            if request.method == "POST":

                album_Id = request.POST.get('album_Id','')
                files = request.FILES.getlist('file')
                for filename in files:
                    save_image = AlbumPhotos(photo=filename, albumPhoto_id=album_Id)
                    save_image.save()

                data = {'status':'true'}
                return HttpResponse(json.dumps(data), content_type="application/json")

    except KeyError:
        pass
    return redirect('/')
"""
