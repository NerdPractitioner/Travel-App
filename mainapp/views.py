from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, ListView
from UserProfiles.models import Profile
from django.contrib.auth.forms import User
# from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404


def home(request):
    return render(request, "home.html")


class SearchResultsView(ListView):
    # /results
    model = User
    template_name = 'user_search.html'

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(object_list=object_list, **kwargs)
    #     return context

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            object_list = User.objects.filter(
                Q(username__icontains=query) |
                Q(first_name__icontains=query)
            )
        else:
            object_list = User.objects.all()
        return object_list

def get_user_profile(request, username):
    user = User.objects.get(username=username)
    #user = get_object_or_404(User, username=self.kwargs.get('username'))
    return render(request,'other_user.html',{"user":user})