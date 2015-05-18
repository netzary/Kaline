from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
import datetime, random, re, os, csv, time
from django.template import Context, Template, loader
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from models import *
from django.forms import ModelForm
from models import *
from ldap_settings import *
from local_ldap import *
from django import forms
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
attrs_dict={}
from slave_settings import *
from tasks import *
import requests
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def check_ldap(request):
    try:
	x =get_user_list()
	try:
	    if x[0]!="server_not_found":
		return HttpResponse("OK")
	
	    else:
		raise Http404
	except:
	    raise Http404
    except ldap.LDAPError, e:
	raise Http404




@csrf_exempt
def api_add_user(request):
    if request.method=="POST":
	secret_key =request.POST.get("secret_key")
	if secret_k ==secret_key:
	    pass
	else:
	    raise Http404
	ip = request.META["REMOTE_ADDR"]
	if ip == master_ip:
	    pass
	else:
	    raise Http404
	
	first_name =request.POST.get("first_name")
	    
	last_name = request.POST.get("last_name")
	username =  request.POST.get("username")
	email =request.POST.get("email")
	uid = request.POST.get("uid")
	if request.POST.get("phone"):
	    phone = request.POST.get("phone")
	else:
	    phone =" "   
	password = request.POST.get("password")
	x=task_add_user(first_name, last_name, username, email,  password, uid, phone)
	return HttpResponse("OK")
    return HttpResponse("OK")
@csrf_exempt
def api_add_group(request):
  
    if request.method=="POST":
	secret_key =request.POST.get("secret_key")
	ip = request.META["REMOTE_ADDR"]
	print secret_key, ip
	if ip == master_ip:
	    pass
	else:
	    raise Http404
	if secret_k == secret_key:
	    pass
	else:
	    raise Http404
	
	name =request.POST.get("name")
	gid =request.POST.get("gid")
	print name, gid
	task_add_group(name, gid)
	return HttpResponse("OK")
    return HttpResponse("OK")
@csrf_exempt
def api_delete_user(request):
    if request.method=="POST":
	secret_key =request.POST.get("secret_key")
	ip = request.META["REMOTE_ADDR"]
	if ip == master_ip:	
	    pass
	else:
	    raise Http404
	if secret_k == secret_key:
	    pass
	else:
	    raise Http404
	user =request.POST.get("user")
	print user
	
	task_delete_user(user)
	return HttpResponse("OK")

    return HttpResponse("OK")
import ast
@csrf_exempt
def api_u2g(request):
    if request.method=="POST":
	secret_key =request.POST.get("secret_key")
	ip = request.META["REMOTE_ADDR"]
	if ip == master_ip:	
	    pass
	else:
	    raise Http404
	if secret_k == secret_key:
	    pass
	else:
	    raise Http404
	gid = request.POST["gid"]
	usernames = request.POST["usernames"]
	group =LdapGroup.objects.get(gid=int(gid))
	group.usernames = ast.literal_eval(usernames)
	return HttpResponse("OK")
    return HttpResponse("OK")
@csrf_exempt
def api_delete_group(request):
    if request.method=="POST":
	secret_key =request.POST.get("secret_key")
	ip = request.META["REMOTE_ADDR"]
    if ip == master_ip:	
        pass
    else:
	raise Http404
    if secret_k == secret_key:
	pass
    else:
	raise Http404
    group = request.POST.get("group")
    task_delete_group(group)
  
    return HttpResponse("OK")


@csrf_exempt
def api_change_password(request):
    print request.POST.items()
    if request.method=="POST":
	print 1
	secret_key =request.POST.get("secret_key")
	ip = request.META["REMOTE_ADDR"]
	if ip == master_ip:	
	    pass
	else:
	    raise Http404
	if secret_k == secret_key:
	    pass
	else:
	    raise Http404
    
	user= request.POST.get("user")
	password = request.POST.get("password")
	print "KK"
	task_change_password(user,password)
	return HttpResponse("OK")

    return HttpResponse("OK")



@csrf_exempt
def api_upload(request):
    if request.method=="POST":
	secret_k =request.POST.get("secret_k")
	ip = request.META["REMOTE_ADDR"]
    if ip == master_ip:	
        pass
    else:
	raise Http404
    if ip == master_ip:
	pass
    else:
	raise Http404

    if request.method=="POST":
	
	handle_uploaded_file(request.FILES['file'])
	return HttpResponse("OK")
	    
	
