import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse
from pally.models import LearnerProfile, PallyneUser, Publisher, PallyneVideo, AssociatedDatasets, ReferenceBook, Subject, Course, Module
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from pally.forms import LoginForm, UserRegistrationForm, PallyUserEditForm, PallyLearnerProfileEditForm
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib import messages, auth

# Pallyne Views
def index(request):
    videos = PallyneVideo.objects.all()[0:4]
    context_dict = {'recentvideos': videos }
    return render(request, 'pally/index.html', context=context_dict)

@login_required
def dashboard(request):
    return render(request, 'pally/dashboard.html', {'section': 'dashboard'})

def register(request):
    if request.user.is_authenticated:
        #return redirect('index', username=request.user.username)
        return render(request, 'pally/dashboard.html', { 'section' : 'dashboard' })

    if request.method == 'POST':
        new_user = UserRegistrationForm(request.POST)
        if new_user.is_valid():
            new_user.save(request)
            context_dict = {}
            return render(request, 'registration/register_done.html', context=context_dict)
    else:
        new_user = UserRegistrationForm()
    return render(request, 'registration/register.html', {'new_user': new_user })

def activate_account(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = PallyneUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, PallyneUser.DoesNotExist):
        user = None
    if (user is not None and default_token_generator.check_token(user, token)):
        user.is_active = True
        user.save()
        messages.add_message(request, messages.INFO, 'Your account has been activated.Please Login')
    else:
        messages.add_message(request, messages.INFO, 'Link Expired. Contact the administrator to activate your account')
    return redirect('login')
    
"""
def register(request):
    if request.method == 'POST':
        pallyuserform = UserRegistrationForm(request.POST)
        if pallyuserform.is_valid():
            new_user = pallyuserform.save(commit=False)
            new_user.set_password(pallyuserform.cleaned_data['password'])
            new_user.save()
            #create an empty profile object for the User
            LearnerProfile.objects.create(user=new_user)
            return render(request, 'registration/register_done.html', {'new_user': new_user })
    else:
        pallyuserform = UserRegistrationForm()
    return render(request, 'registration/register.html', {'pallyuserform': pallyuserform})
"""
@login_required
def editprofile(request):
    if request.method == 'POST':
        pally_user_form = PallyUserEditForm(instance=request.user, data=request.POST)
        pally_learner_profile_form = PallyLearnerProfileEditForm(instance=request.user.learnerprofile, data=request.POST, files=request.FILES)
        if pally_user_form.is_valid() and pally_learner_profile_form.is_valid():
            pally_user_form.save()
            pally_learner_profile_form.save()
            messages.success(request, 'Your profile has been updated successsfully')
        else:
            messages.error(request, 'We encountered an error while updating your profile')
    else:
        pally_user_form = PallyUserEditForm(instance=request.user)
        pally_learner_profile_form = PallyLearnerProfileEditForm(instance=request.user.learnerprofile)

    return render(request, 'pally/editprofile.html', {'pally_user_form' : pally_user_form, 'pally_learner_profile_form' : pally_learner_profile_form})



def pallynelogin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cleaneddata = form.cleaned_data
            user = authenticate(request, username=cleaneddata['username'], password=cleaneddata['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated Successfully')
                else:
                    return HttpResponse('Disabled Account')
            else:
                return HttpResponse('Invalid Login')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', { 'form': form })

@login_required
def pallynevideos(request):
    pallynevideos = PallyneVideo.objects.all() #get all videos in pallyne
    context_dict = {'videos':pallynevideos}
    return render(request, 'pally/pallynevideos.html', context=context_dict)

@login_required
def pallynebooks(request):
    pallybooks = ReferenceBook.objects.all()
    pallynedatasets = AssociatedDatasets.objects.all()[0:5]
    context_dict = {'books': pallybooks, 'datasets':pallynedatasets}
    return render(request, 'pally/pallynebooks.html', context=context_dict)

@login_required
def pallynedatasets(request):
    pallynedatasets = AssociatedDatasets.objects.all()
    context_dict = {'datasets': pallynedatasets}
    return render(request, 'pally/pallynedatasets.html', context=context_dict)

@login_required
def viewvideo(request, video_name_slug):
    context_dict = {}
    try:
        singlevideo = PallyneVideo.objects.get(slug=video_name_slug)
        # Get video with the supplied slug
        context_dict ={'video':singlevideo}
    except PallyneVideo.DoesNotExist:
        context_dict['video'] = None
    return render(request, 'pally/viewvideo.html', context=context_dict)

@login_required
def pallyneuserprofile(request):
    context_dict = {}
    return render(request, 'pally/myprofile.html', context=context_dict)
