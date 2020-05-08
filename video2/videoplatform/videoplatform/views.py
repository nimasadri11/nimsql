import os
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.views.generic.list import ListView
from django.http import Http404, HttpResponse
from infinite_scroll_pagination import paginator
from infinite_scroll_pagination import serializers
from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.forms import PasswordChangeForm
from django.http import FileResponse
from .models import *
from .utils import *
from datetime import datetime
from formtools.wizard.views import SessionWizardView
import random
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView
import datetime as dt
from django.shortcuts import get_object_or_404

talents = [{"Logan Paul": "loganpaul"}, {"Shane Dawson": "shanedawson"}, {"KSI": "KSI"}, {"PewDiePie": "pewdiepie"}, {"Nelk": "nelk"}, {"Steve Will Do It": "stevewilldoit"}]



def home(request):
    context = {}
    context["talents"] = get_creators()
    context['videos'] = get_videos(6)
    return render(request, 'home.html', context)


def logoutUser(request):
    print("++++++")
    context = {"message": "logged out succesfuly"}
    context["talents"] = get_creators()
    if request.user.is_authenticated:
        logout(request)
    # return render(request, 'home.html', context)
    return redirect("/")

def signin(request):
    context = {}
    context["talents"] = get_creators()
    if request.user.is_authenticated:

        context['message'] = ("already logged in as " + str(request.user))
        return redirect("/")
        # return render(request, 'home.html', context)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            #context['message'] = ("succesfuly logged in as " + username)
            return redirect("/")
            # return render(request, 'home.html', context)
        else:
            form = AuthenticationForm(request.POST)
            context['form'] = form
            context['message'] = "bad credentials"
            return render(request, 'login.html', {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})



def signup(request):
    context = {}
    context["talents"] = get_creators()
   # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = UserForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            print("+++form is valid++++")
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            if User.objects.filter(username=email).exists():
                context['message'] = "An account with email " + email + " already exists!"
                context['form'] = UserForm()
                return render(request, "signup.html", context)
            else:
                user = User.objects.create_user(email, password=password)

            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return redirect('/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = UserForm()
    context['form'] = form
    return render(request, 'signup.html', context)




def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return render(request, "home.html")
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'account/change_password.html', {
        'form': form
    })

@login_required
def account(request):
    context = {}
    context["talents"] = get_creators()

    if request.method == 'POST':
        return render(request, "account/account.html", context)
    else:
        return render(request, 'account/account.html', context)


    
    

def error404(request, exception):
    print("+++++++")
    return render(request, '404error.html')


def dashboard_analytics(request, *args, **kwargs):
    context = {}
    views_data = []
    likes_data = []
    dislikes_data = []
    comments_data = []


    for i in range(30):
        views_data.append(random.randint(600000,1000000))
        likes_data.append(random.randint(600000,1000000))
        dislikes_data.append(random.randint(600000,1000000))
        comments_data.append(random.randint(600000,1000000))
        
    base = datetime(year=2018,month=1,day=1)

    labels = [(base + dt.timedelta(days=x)).strftime("%Y-%m-%d") for x in range(30)]
    
    context['dates'] = labels
    context['viewsData'] = views_data
    context['likesData'] = likes_data
    context['dislikesData'] = dislikes_data
    context['commentsData'] = comments_data
    context['countries'] = [{"name": "USA", "percentage": 60}, {"name": "Canada", "percentage": 20}, {"name": "UK", "percentage": 10}, {"name": "Denmark", "percentage": 6}, {"name": "China", "percentage": 4}]


    return render(request, 'dashboard/analytics.html', context)

def dashboard_upload(request, *args, **kwargs):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            
            title = request.POST["title"]
            description = request.POST["description"]
            uploadtime = datetime.now()
            creator_name = "Logan"
            
            video_key = get_url(title + creator_name + request.FILES['videoFile'].name)
            thumbnail_key = get_url(title + creator_name + request.FILES['thumbnailFile'].name)
            upload_s3(request.FILES['videoFile'], "videos/" + video_key)
            upload_s3(request.FILES['thumbnailFile'], "thumbnails/" + thumbnail_key)
            
            creator = Creator.objects.get(page_name="Logan Paul")
            new_video = Video.objects.create(title=title, description=description, uploadtime=uploadtime, url=video_key, thumbnail=thumbnail_key)
            new_video.creator.add(creator)
            

            # print(form.cleaned_data["title"])
            print(request)
            messages.info(request, 'Upload completed!')
            print("good")
            return redirect('/dashboard')
        else:
            print("invalid")
            print(request.FILES)
        
    else:
        form = UploadFileForm()
    return render(request, 'dashboard/upload.html', {'form': form})




class VideoView(ListView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["talents"] = get_creators()
        videos = context["videos"]
        return context
    def get_ordering(self):
        ordering = self.request.GET.get('sort', 'uploadtime')
        return "-" + ordering
    paginate_by = 1
    queryset = get_videos()
    context_object_name = 'videos'
    template_name = 'videos.html'
    


class CreatorVideoView(ListView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["talents"] = get_creators()
        videos = context["videos"]
        return context
    def get_ordering(self):
        ordering = self.request.GET.get('sort', 'uploadtime')
        print("Ordering: " + ordering)
        return "-" + ordering
    paginate_by = 1
    queryset = get_videos()
    context_object_name = 'videos'
    template_name = 'creator.html'
    


def play(request, *args, **kwargs):
    context = {}
    context["talents"] = get_creators()
    video_id = request.GET.get('videoId')
    context["video"] = Video.objects.get(url=video_id)
    return render(request, 'play.html', context)

def join(request):
    return render(request, 'join.html')

    
    
class SubscribeWizard(SessionWizardView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["talents"] = get_creators()
        context["videos"] = get_videos(6)
        return context
    def get_template_names(self):
        
        if self.steps.current == "0":
            return "home.html"
        elif self.steps.current == "1":
            return "join.html"
        elif self.steps.current == "2":
            return "plans.html"
    def done(self, form_list, **kwargs):
        print(form_list)
        return redirect('/videos')



def dashboard_manage(request):
    context = {}
    print(request)
    if request.method == 'POST':
        bannerForm = ChangeBannerForm(request.POST, request.FILES)
        if bannerForm.is_valid():
            print(bannerForm)

        else:
            print(bannerForm)


    else:
        bannerForm = ChangeBannerForm()
        profilePhotoForm = ChangeProfilePhotoForm()
    context['bannerForm'] = bannerForm
    context['profilePhotoForm'] = profilePhotoForm
    context['videos'] = get_videos()
    return render(request, 'dashboard/manage.html', context)
    

def dashboard_support(request):
    context = {}
    return render(request, 'dashboard/support.html', context)

    

def dashboard_manage_video(request, *args, **kwargs):
    context = {}
    context["talents"] = get_creators()
    video_id = request.GET.get('videoId')
    context["video"] = Video.objects.get(url=video_id)
    instance = Video.objects.get(url=video_id)
    print(request.FILES)
    form = VideoEdit(request.POST or None, request.FILES or None, instance=instance)
    print(form)
    if request.method == 'POST':
        try:
            form.thumbnailFile = request.FILES["thumbnailFile"]
        except KeyError:
            form.thumbnailFile = None
    if form.is_valid():
        print('valid-------')
        form.save()
        return redirect('/dashboard')
    context['form'] = form
    return render(request, 'dashboard/manage_video.html', context) 

    # return render(request, 'dashboard/manage_video.html', context)

def delete_video(request):
    context = {}
    context["talents"] = get_creators()
    video_id = request.GET.get('videoId')
    print("deleting")
    Video.objects.filter(url=video_id).delete()
    return redirect("/dashboard")