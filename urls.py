from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
################################3
urlpatterns = patterns('',
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),  (r'^base/$', 'ldapman.views.base'), (r'^$', 'ldapman.views.base'),
    
    (r'^users/add/$', 'ldapman.views.add_user'),
     (r'^groups/add/$', 'ldapman.views.add_group'), (r'^groups/addusers/(?P<group>.*)/$', 'ldapman.views.add_users_to_group_form'),
     (r'^groups/users2groups/(?P<group>.*)/$', 'ldapman.views.users2groups'),
     (r'^users/$', 'ldapman.views.users'), (r'^groups/$', 'ldapman.views.groups'),
      (r'^groups/delete/(?P<group>.*)/$', 'ldapman.views.delete_group') ,(r'^users/delete/(?P<user>.*)/$', 'ldapman.views.delete_user'),
       (r'^change_password/(?P<user>.*)/$', 'ldapman.views.change_password'),
              (r'^user_change_password/$', 'ldapman.views.user_change_password'),
       (r'^upload/$', 'ldapman.views.upload'),        (r'^post_login/$', 'ldapman.views.post_login'), 
         (r'^last_logins/$', 'ldapman.views.last_logins'), (r'^inactive_logins/$', 'ldapman.views.inactive_accounts'), 
	 
	 (r'^get_p_time/(?P<uid>.*)$', 'ldapman.views.get_password_time'), 
)
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views 



urlpatterns += staticfiles_urlpatterns()



urlpatterns += patterns('',
 (r'^api_users/add/$', 'ldapman.api_views.api_add_user'),
     (r'^api_groups/add/$', 'ldapman.api_views.api_add_group'), #
     #(r'^groups/users2groups/(?P<group>.*)/$', 'ldapman.views.users2groups'),
     
      (r'^api_groups/delete/$', 'ldapman.api_views.api_delete_group') ,
      (r'^api_users/delete/$', 'ldapman.api_views.api_delete_user'),
      
       (r'^api_change_password/$', 'ldapman.api_views.api_change_password'),
       (r'^api_user2groups/$', 'ldapman.api_views.api_u2g'),
       (r'^api_upload/$', 'ldapman.api_views.api_upload'), 
        (r'^check_ldap/$', 'ldapman.api_views.check_ldap'), 


)

urlpatterns += patterns('',
                   
                        url(r'^accounts/login/$',
                           auth_views.login,
                           {'template_name': 'registration/login.html'},
                           name='auth_login'),
                       url(r'^accounts/logout/$',
                           auth_views.logout,
                           {'template_name': 'registration/logout.html'},
                           name='auth_logout'),
                       url(r'^accounts/password/change/$',
                           auth_views.password_change,
			    {'template_name': 'registration/password_reset_form.html'},
                           name='auth_password_change'),
                       url(r'^accounts/password/change/done/$',
                           auth_views.password_change_done,
                           name='auth_password_change_done'),
                       url(r'^accounts/password/reset/$',
                           auth_views.password_reset,
			      {'template_name': 'registration/password_reset_form.html'},
                           name='auth_password_reset'),
                       url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
                           auth_views.password_reset_confirm,
                           name='auth_password_reset_confirm'),
                       url(r'^accounts/password/reset/complete/$',
                           auth_views.password_reset_complete,
                           name='auth_password_reset_complete'),
                       url(r'^accounts/password/reset/done/$',
                           auth_views.password_reset_done,
                           name='auth_password_reset_done'),
              
		       )

