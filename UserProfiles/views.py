import os as os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from PIL import Image
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from django.forms import modelformset_factory
from django.urls import reverse
from .models import Images, Profile
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


from django.contrib.auth.models import User

"""
@login_required
class UserDetailView(DetailView):
    u = 
    model = User
    slug_field = 'username'
    slug_url_kwargs = 'username'
"""
"""
def index(request):
    path = settings.MEDIA_ROOT
    img_list = os.listdir(path + '/images')
    context = {'images' : img_list}
    return render(request, "photo/index.html", context)



class UserUpdateView(LoginRequiredMixin, UpdateView):
    fields = ['name', 'email', 'picture', 'job_title', 'location', 'personal_url',
              'facebook_account', 'twitter_account', 'github_account',
              'linkedin_account', 'short_bio', 'bio', ]
    model = User

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)



#VITOR METHOD


from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView




class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})


class UserUpdateView(LoginRequiredMixin, UpdateView):
    fields = ['name', 'email', 'picture', 'job_title', 'location', 'personal_url',
              'facebook_account', 'twitter_account', 'github_account',
              'linkedin_account', 'short_bio', 'bio', ]
    model = User

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)


class UserListView(LoginRequiredMixin, ListView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'
























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


@login_required
def get_user_profile (request, user):
    # If no such user exists raise 404
    #other_user = username
    # Flag that determines if we should show editable elements in template
   # editable = False
    # Handling non authenticated user for obvious reasons
   # if request.user.is_authenticated() and request.user.username == user:
    #    editable = True
    if request.user.username == user:
        profile = get_object_or_404(User, user=request.user)
        return render(request, 'UserProfiles/profile.html', {'profile': profile})
    else:
        raise Http404
    #return render (request, 'UserProfiles/profile.html', {'other_user':other_user})


"""