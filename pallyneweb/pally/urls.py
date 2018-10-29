from django.conf.urls import url
from pally import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^&', views.dashboard, name='dashboard'),
    url(r'^pallynevideos/$', views.pallynevideos, name='pallynevideos'),
    url(r'^pallynebooks/$', views.pallynebooks, name='pallynebooks'),
    url(r'^pallynedatasets/$', views.pallynedatasets, name='pallynedatasets'),
    url(r'^viewvideo/(?P<video_name_slug>[\w\-]+)/$', views.viewvideo, name='viewvideo'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^password_reset/$', auth_views.password_reset, \
        {'template_name': 'registration/password_reset_form.html',
         'email_template_name': 'registration/email/password_reset_email.txt',
         'subject_template_name': 'registration/email/password_reset_subject.txt',
         'post_reset_redirect': 'password_reset_done'}, name='password_reset'),

    url(r'^password_reset_done/$', auth_views.password_reset_done, \
        {'template_name': 'registration/password_reset_done.html',}, name='password_reset_done'),

    url(r'^password_confirm/'
        r'(?P<uidb64>[0-9A-Za-z_\-]+)/'
        r'(?P<token>[0-9A-Za-z]{1,13}'
        r'-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm,
        {'template_name': 'registration/password_reset_confirm.html',
        'post_reset_redirect': 'password_reset_complete'},
        name='password_reset_confirm'),

    url(r'^password_reset_complete/$', auth_views.password_reset_complete,
        {'template_name': 'registration/password_reset_complete.html'}, name='password_reset_complete'),

    url(r'^register/$', views.register, name='register'),
    url(r'^activate/'
        r'(?P<uidb64>[0-9A-Za-z_\-]+)/'
        r'(?P<token>[0-9A-Za-z]{1,13}'
        r'-[0-9A-Za-z]{1,20})/$',
        views.activate_account, name='activate'),
    
    url(r'^editprofile/$', views.editprofile, name='editprofile'),
    url(r'^pallyneuserprofile/$', views.pallyneuserprofile, name='pallyneuserprofile'),

]
