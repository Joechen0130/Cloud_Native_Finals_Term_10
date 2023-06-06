from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from fms_django.settings import MEDIA_ROOT, MEDIA_URL
import json
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from fmsApp.forms import UserRegistration, SavePost, UpdateProfile, UpdatePasswords
from fmsApp.models import Post
from cryptography.fernet import Fernet
from django.conf import settings
import base64
from django.views.generic import ListView

# Create your views here.
#0429 decorator
from django.http import Http404
from django.views import View
# from .filters import PostFilter

import logging
# Get an instance of a logger
logger = logging.getLogger('custom_logger')
logger.setLevel(logging.INFO)


def check_user_able_to_delete_file(*groups):
    def decorator(function):
        def wrapper(request, *args, **kwargs):
            if request.user.groups.filter(name__in=groups).exists():
                return function(request, *args, **kwargs)
            raise Http404
        return wrapper
    return decorator

##################################################

context = {
    'page_title' : 'File Management System',
}

#login
def login_user(request):
    logger.info('Get login request.')
    logout(request)
    resp = {"status":'failed','msg':''}
    username = ''
    password = ''
    if request.POST:
        logger.info('Post login.')
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                resp['status']='success'
                logger.info('Success login')
            else:
                resp['msg'] = "Incorrect username or password"
                logger.info('Incorrect username or password')
        else:
            resp['msg'] = "Incorrect username or password"
            logger.info('Incorrect username or password')
    return HttpResponse(json.dumps(resp),content_type='application/json')

#Logout
def logoutuser(request):
    logger.info('Get logout request.')
    logout(request)
    return redirect('/')

@login_required
def home(request):
    logger.info('Get home page request.')
    context['page_title'] = 'Home'
    if request.user.is_superuser:
        logger.debug('Admin user.')
        posts = Post.objects.all()
    else:
        logger.debug('Normal user.')
        query_set = Group.objects.filter(user = request.user).all()
        for g in query_set:
            logger.debug(g.name)
            group_n= g.name
        g = Group.objects.get(name=group_n)
        users_name = g.user_set.all()
        users_name_list = list(users_name)
        posts = Post.objects.filter(user__in = users_name_list).all()
    context['posts'] = posts
    context['postsLen'] = posts.count()
    #print(request.build_absolute_uri())
    return render(request, 'home.html',context)

@login_required
def public(request):
    logger.info('Get public page request.')
    context['page_title'] = 'Public'
    id = User.objects.get(username='pub_demo').pk
    # print(id)
    posts = Post.objects.filter(user=id)
    context['posts'] = posts
    context['postsLen'] = posts.count()
    #print(request.build_absolute_uri())
    return render(request, 'public.html',context)


class PollHistoryView(ListView, View):
    template_name = "history.html"
    logger.info('Get history page request.')
    def get_queryset(self):
        if self.request.user.is_superuser:
            history = Post.history.all()
        else:
            query_set = Group.objects.filter(user = self.request.user).all()
            for g in query_set:
                #print(g.name)
                logger.debug(f'{g.name}.')
                group_n= g.name
                g = Group.objects.get(name=group_n)
                users_name = g.user_set.all()
                users_name_list = list(users_name)
                history = Post.history.filter(user__in = users_name_list).all()
                # history = Post.history.filter(user = self.request.user).all()
        return history

    
def registerUser(request):
    logger.info('Get register request.')
    user = request.user
    if user.is_authenticated:
        logger.info('Get in System.')
        return redirect('home-page')
    context['page_title'] = "Register User"
    if request.method == 'POST':
        logger.info('Post register page.')
        data = request.POST
        form = UserRegistration(data)
        if form.is_valid():
            # form.save()
            # 0429#####
            user = form.save(commit=False)
            user.save()
            ################
            username = form.cleaned_data.get('username')
            pwd = form.cleaned_data.get('password1')
            groups = form.cleaned_data.get('groups')
            user_group = Group.objects.get(name=groups) 
            user.groups.add(user_group)
            loginUser = authenticate(username= username, password = pwd)
            login(request, loginUser)
            logger.info('Get in System.')
            return redirect('home-page')
        else:
            context['reg_form'] = form

    return render(request,'register.html',context)

@login_required
def profile(request):
    logger.info('Get profile page request.')
    context['page_title'] = 'Profile'
    return render(request, 'profile.html',context)

@login_required
def posts_mgt(request):
    logger.info('Get post list request.')
    context['page_title'] = 'Uploads'
    posts = Post.objects.filter(user = request.user).order_by('title', '-date_created').all()
    context['posts'] = posts
    return render(request, 'posts_mgt.html', context)

@login_required
def manage_post(request, pk=None):
    context['page_title'] = 'Manage Post'
    context['post'] = {}
    if not pk is None:
        post = Post.objects.get(id = pk)
        context['post'] = post
    return render(request,'manage_post.html',context)

@login_required
def save_post(request):
    logger.info('Get save file request.')
    resp = {'status':'failed', 'msg':''}
    if request.method == 'POST':
        logger.info('Post save/change file.')
        if not request.POST['id'] == '':
            post = Post.objects.get(id=request.POST['id'])
            form = SavePost(request.POST,request.FILES,instance=post)
        else:
            form = SavePost(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            logger.info('File has been saved successfully!')
            messages.success(request,'File has been saved successfully.')
            resp['status'] = 'success'
        else:
            for fields in form:
                for error in fields.errors:
                    logger.error(str( error +'<br/>'))
                    resp['msg'] += str( error +'<br/>')
            form = SavePost(request.POST,request.FILES)
            
    else:
        logger.warning("No data sent")
        resp['msg'] = "No Data sent."
    #print(resp)
    return HttpResponse(json.dumps(resp),content_type="application/json")

@login_required
def delete_post(request):
    logger.info("Get delete file request")
    resp = {'status':'failed', 'msg':''}
    if request.method == 'POST':
        logger.info('Post delete file.')
        try:
            post = Post.objects.get(id = request.POST['id'])
            post.delete()
            logger.info("Successfully delete file")
            resp['status'] = 'success'
            messages.success(request, 'Post has been deleted successfully')
        except:
            logger.warning("Undefined Post ID")
            resp['msg'] = "Undefined Post ID"
    return HttpResponse(json.dumps(resp),content_type="application/json")

def shareF(request,id=None):
    # print(str("b'UdhnfelTxqj3q6BbPe7H86sfQnboSBzb0irm2atoFUw='").encode())
    context['page_title'] = 'Shared File'
    if not id is None:
        key = settings.ID_ENCRYPTION_KEY
        fernet = Fernet(key)
        id = base64.urlsafe_b64decode(id)
        id = fernet.decrypt(id).decode()
        post = Post.objects.get(id = id)
        context['post'] = post
        context['page_title'] += str(" - " + post.title)
   
    return render(request, 'share-file.html',context)

@login_required
def update_profile(request):
    logger.info("Get update profile request")
    context['page_title'] = 'Update Profile'
    user = User.objects.get(id = request.user.id)
    if not request.method == 'POST':
        form = UpdateProfile(instance=user)
        context['form'] = form
        #print(form)
    else:
        form = UpdateProfile(request.POST, instance=user)
        if form.is_valid():
            form.save()
            logger.info("Profile has been updated")
            messages.success(request, "Profile has been updated")
            return redirect("profile")
        else:
            context['form'] = form
            
    return render(request, 'manage_profile.html',context)


@login_required
def update_password(request):
    logger.info("Get update password request")
    context['page_title'] = "Update Password"
    if request.method == 'POST':
        logger.info('Post update password')
        form = UpdatePasswords(user = request.user, data= request.POST)
        if form.is_valid():
            form.save()
            logger.info("Your Account Password has been updated successfully")
            messages.success(request,"Your Account Password has been updated successfully")
            update_session_auth_hash(request, form.user)
            return redirect("profile")
        else:
            logger.warning("Your Account Password has been not updated successfully")
            context['form'] = form
    else:
        form = UpdatePasswords(request.POST)
        context['form'] = form
    return render(request,'update_password.html',context)



