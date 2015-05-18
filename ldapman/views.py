from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
import datetime, random, re, os, csv
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
import requests, json


def check_slaves():
    if len(slave_ips)>0:
	for ip in slave_ips:
	    url ="http://%s:%s/check_ldap/" %(ip, str(port))
	    x=requests.get(url)
	    if int(x.status_code)==200:
		pass 
	    else:
		return False
    return True




def base(request):
    return render_to_response("base.html", context_instance=RequestContext(request))



class UPasswordForm(forms.Form):
    
    def __init__(self,  *args, **kwargs):
        super(UPasswordForm, self).__init__(*args, **kwargs)
	
	self.fields["user"] = forms.CharField(max_length=30,
                                label=_(u'Enter Your LDAP Username'))
	self.fields["password"] =forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label=_(u'Old/Existing Password'))
	self.fields["password1"]= forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label=_(u'New Password'))
	self.fields["password2"] = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label=_(u'New password (again)'))
                                
                                
    def clean(self):

        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_(u'You must type the same password each time'))
	if 'user' in  self.cleaned_data and 'password' in self.cleaned_data:
	    user = self.cleaned_data['user']
	    dn =find_dn(user)
	    print dn
	    password =self.cleaned_data['password']
	    print password
	    l = ldap.initialize(server)
	    try:	    
		l.simple_bind_s(dn, password)
	    except Exception, error:
		raise forms.ValidationError(_(u'Your current LDAP username and password not matching!'))
        
	return self.cleaned_data    
    def clean_password1(self):
	if self.cleaned_data["password1"]:
	    exp1 ="^(?=.*[A-Z])(?=.*[0-9])(?=.*[a-z]).{8,16}$"
	    exp2 ="^(?=.*[A-Z])(?=.*[!@#$&*])(?=.*[a-z]).{8,16}$"
	    exp3 ="^(?=.*[A-Z])(?=.*[!@#$&*])(?=.*[0-9]).{8,16}$"
	    exp4 = "^(?=.*[!@#$&*])(?=.*[0-9])(?=.*[a-z]).{8,16}$"
	    passw = self.cleaned_data["password1"]
	    if ( re.match(exp1,passw) or re.match(exp2,passw) or re.match(exp3,passw) or re.match(exp4,passw)) !=None:
		pass
	    else:
		raise 	 forms.ValidationError("The Password needs to meet 3 out 4 criteria. 1 Special Character, 1 Capital Letter, 1 Numeral and 1 small letter. Minimum Length 8")
	return self.cleaned_data["password1"]


def user_change_password(request):
    if request.method=="POST":
	form =UPasswordForm(request.POST)
	if form.is_valid():
	    user=form.cleaned_data["user"]
	    dn=find_dn(user)
	    password =form.cleaned_data["password1"]
	    u =LdapUser.objects.get(username=user)
	    uid =u.uid
	    x=change_p(dn,password)
	    if slave ==False:
		if len(slave_ips)>0:
		    for ip in slave_ips:
			url ="http://%s:%s/api_change_password/" %(ip, str(port))
			payload ={"secret_key":secret_k, "user":user, "password": password}
			requests.post(url,payload)

	    if x ==1:
		try:
		    
		    pman = PasswordManager.objects.get(user=uid)
		    pman.time =datetime.datetime.today()
		    pman.save()
		except PasswordManager.DoesNotExist:
		    pman = PasswordManager()
		    pman.user =uid
		    pman.time =datetime.datetime.today()
		    pman.save()
		return HttpResponseRedirect("/users/")
	    else:
		return HttpResponse("Some Error has Occured")
	    return HttpResponseRedirect("/")
    else:
	form = UPasswordForm()
    return render_to_response("password.html", {"form":form}, context_instance=RequestContext(request))

	    


class UserForm(forms.Form):
    username = forms.CharField(max_length=30, required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name= forms.CharField(max_length=30, required=True)
    email = forms.EmailField( required=True)
    phone = forms.IntegerField( required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label=_(u'New Password'))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label=_(u'New password (again)'))
				
    def clean(self):
        """
        Verifiy that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.
       
        """
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_(u'You must type the same password each time'))
        return self.cleaned_data    

    def clean_username(self):
	if self.cleaned_data["username"]:
	    uname =self.cleaned_data["username"]
	    users = get_user_list()
	    if uname in users:
		raise forms.ValidationError("There's a user registered with this username. Choose another Name")
	return self.cleaned_data["username"]
	
    def clean_password1(self):
	if self.cleaned_data["password1"]:
	    exp1 ="^(?=.*[A-Z])(?=.*[0-9])(?=.*[a-z]).{8,16}$"
	    exp2 ="^(?=.*[A-Z])(?=.*[!@#$&*])(?=.*[a-z]).{8,16}$"
	    exp3 ="^(?=.*[A-Z])(?=.*[!@#$&*])(?=.*[0-9]).{8,16}$"
	    exp4 = "^(?=.*[!@#$&*])(?=.*[0-9])(?=.*[a-z]).{8,16}$"
	    passw = self.cleaned_data["password1"]
	    if ( re.match(exp1,passw) or re.match(exp2,passw) or re.match(exp3,passw) or re.match(exp4,passw)) !=None:
		pass
	    else:
		raise 	 forms.ValidationError("The Password needs to meet 3 out 4 criteria. 1 Special Character, 1 Capital Letter, 1 Numeral and 1 small letter. Minimum Length 8")
	return self.cleaned_data["password1"]
		

	    
class GroupForm(forms.Form):
    name = forms.CharField(max_length=30, required=True)

    
    def clean_name(self):
	if self.cleaned_data["name"]:
	    uname =self.cleaned_data["name"]
	    users = get_group_list()
	    if uname in users:
		raise forms.ValidationError("There's a group registered with this name. Choose another Name")
	return self.cleaned_data["name"]
	


@login_required
def add_user(request):
    if slave==True:
	message = "I am slave go to my master on %s" % (master_ip)
	return HttpResponse(message)
    if request.method=="POST":
	form =UserForm(request.POST)
	if form.is_valid():
	    #return HttpResponse(request.POST.items())
	    user=LdapUser()
	    user.first_name =request.POST.get("first_name")
	    
	    user.last_name = request.POST.get("last_name")
	    user.full_name = request.POST.get("first_name") +"  " + request.POST.get("last_name")
	    uname =  request.POST.get("username")
	    user.username =uname
	    user.email =email=request.POST.get("email")
	    user.group = base_group
	    user.gecos = user.full_name
	    if request.POST.get("phone"):
		user.phone = phone= request.POST.get("phone")
	    else:
		phone = " " 
	    
	    #return HttpResponse(user.username +" " " " + user.gecos +"  " + str(base_group) + " " + user.gecos)
	    uids =[u.uid for u in LdapUser.objects.all()] 
	    #return HttpResponse(str(uids))
	    if  len(uids)!=0:
		uid_max = max(uids)
	    else:
		uid_max =uid_start 
	    user.uid = uid_max +1
	    uid =user.uid
	    #return HttpResponse(str(user.uid))
	    user.home_directory = os.path.join(home_start_path, user.username)
	    #return HttpResponse(user.username +" " + str(uid_max) + " " + user.gecos +"  " + str(base_group) + " " + user.home_directory)
	    user.save()
	    password1 = form.cleaned_data["password1"]
	    dn =find_dn(user.username)
	    x= change_p(dn, password1)
	    try:
		pman = PasswordManager.objects.get(user=uid)
		pman.time =datetime.datetime.today()
		pman.save()
	    except PasswordManager.DoesNotExist:
		pman = PasswordManager()
		pman.user =uid
		pman.time =datetime.datetime.today()
		pman.save()
	    if slave ==False:
		if len(slave_ips)>0:
		    for ip in slave_ips:
			url ="http://%s:%s/api_users/add/" %(ip, str(port))
			payload ={"secret_key":secret_k, "uid":user.uid, "email":email, "first_name":user.first_name,
			"last_name":user.last_name, 
			"username": user.username,
			"password":password1,}
			if phone !=None:
			    payload["phone"] =str(phone)
			requests.post(url,payload)
			
			
	    return HttpResponseRedirect("/users/")
    else:
	form =UserForm()
    return render_to_response("add_user.html", {"form":form}, context_instance=RequestContext(request))
	    
@login_required    
def add_group(request):
    return HttpResponse("Since this is a restricted, this feature has been disabled")
    if slave==True:
	message = "I am slave go to my master on %s" % (master_ip)
	return HttpResponse(message)
    if request.method=="POST":
	form =GroupForm(request.POST)
	if form.is_valid():
	    f=LdapGroup()
	    f.name = request.POST.get("name")
	    uids =[u.gid for u in LdapGroup.objects.all()] 
	    #return HttpResponse(str(uids))
	    if  len(uids)!=0:
		uid_max = max(uids)
	    else:
		uid_max =gid_start 
	    f.gid = uid_max +1
	    f.save()
	    if slave ==False:
		if len(slave_ips)>0:
		    for ip in slave_ips:
			url ="http://%s:%s/api_groups/add/" %(ip, str(port))
			payload ={"secret_key":secret_k, "gid":f.gid, "name":f.name}

			requests.post(url,payload)
			
	    return HttpResponseRedirect("/groups/addusers/"+ f.name +"/")
    else:
	form =GroupForm()
    return render_to_response("add_group.html", {"form":form}, context_instance=RequestContext(request))
	    
@login_required    
def add_users_to_group_form(request, group):
    if slave==True:
	message = "I am slave go to my master on %s" % (master_ip)
	return HttpResponse(message)
    group = get_object_or_404(LdapGroup, name__exact=group)
    existing = group.usernames
    users = get_user_list()
    others =[u for u in users if u not in existing]
    return render_to_response("user2g_form.html", { "existing": existing, "users":users, "others": others, "group":group },  context_instance=RequestContext(request))

@login_required
def users2groups(request, group):
    return HttpResponse("Since this is a restricted, this feature has been disabled")

    if slave==True:
	message = "I am slave go to my master on %s" % (master_ip)
	return HttpResponse(message)
    group = get_object_or_404(LdapGroup, name__exact=group)
    if request.method== "POST":
	keys = request.POST.keys()
	users = get_user_list()
	group.usernames=[]
	for key in keys:
	    if (key in users):
		group.usernames.append(key)
	group.save()
	if slave ==False:
	    if len(slave_ips)>0:
		for ip in slave_ips:
		    url ="http://%s:%s/api_user2groups/" %(ip, str(port))
		    payload ={"secret_key":secret_k, "gid":f.gid, "usernames":str(group.usernames)}

		    requests.post(url,payload)
	return HttpResponseRedirect("/groups/")
    else:
	return HttpResponse(" ")

@login_required
def groups(request):
    return HttpResponse("Since this is a restricted, this feature has been disabled")

    groups =LdapGroup.objects.all()
    return render_to_response("groups.html", {"object_list": groups}, context_instance=RequestContext(request))
@login_required
def users(request):
    users =get_user_list()
    groups =LdapUser.objects.all()
    ob=[]
    #users.sort()
    for user in users:
	dic={}
	dic["username"]= user
	ob.append(dic)
    return render_to_response("users.html", {"object_list": ob}, context_instance=RequestContext(request))
@login_required
def delete_user(request, user):
    if slave==True:
	message = "I am slave go to my master on %s" % (master_ip)
	return HttpResponse(message)
    try:
	u =  LdapUser.objects.get(username__exact = user)
	u.delete()
    except LdapUser.DoesNotExist:
	return HttpResponseRedirect("This user has not been created with the application Netzary LDAP Manager.Always create users with Netzary. It's not deleted")
    if slave ==False:
	if len(slave_ips)>0:
	    for ip in slave_ips:
		url ="http://%s:%s/api_users/delete/" %(ip, str(port))
		payload ={"secret_key":secret_k, "user":user}
		requests.post(url,payload)
    return HttpResponseRedirect("/users/")


@login_required
def delete_group(request, group):
    return HttpResponse("Since this is a restricted, this feature has been disabled")

    if slave==True:
	message = "I am slave go to my master on %s" % (master_ip)
	return HttpResponse(message)
    group =  get_object_or_404(LdapGroup, name__exact = group)
    if len(group.usernames) == 0:
	group.delete()
	if slave ==False:
	    if len(slave_ips)>0:
		for ip in slave_ips:
		    url ="http://%s:%s/api_groups/delete/" %(ip, str(port))
		    payload ={"secret_k":secret_k, "group":group.name}
		    requests.post(url,payload)

	return HttpResponseRedirect("/groups/")
    else:
	return HttpResponse("You can only delete Empty Groups")
    

class ChangePasswordForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label=_(u'New Password'))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label=_(u'New password (again)'))
				
    def clean(self):
        """
        Verifiy that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.
       
        """
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_(u'You must type the same password each time'))
        return self.cleaned_data    

@login_required
def change_password(request, user):
    if slave==True:
	message = "I am slave go to my master on %s" % (master_ip)
	return HttpResponse(message)
    if request.method=="POST":
	form = ChangePasswordForm(request.POST)
	if form.is_valid():
	    password1= form.cleaned_data["password1"]
	    dn =find_dn(user)
	    x= change_p(dn, password1)
	    u =LdapUser.objects.get(username=user)
	    uid =u.uid

	    if slave ==False:
		if len(slave_ips)>0:
		    for ip in slave_ips:
			url ="http://%s:%s/api_change_password/" %(ip, str(port))
			payload ={"secret_key":secret_k, "user":user, "password": password1}
			requests.post(url,payload)

	    if x ==1:
		try:
		    pman = PasswordManager.objects.get(user=uid)
		    pman.time =datetime.datetime.today()
		    pman.save()
		except PasswordManager.DoesNotExist:
		    pman = PasswordManager()
		    pman.user =uid
		    pman.time =datetime.datetime.today()
		    pman.save()
		return HttpResponseRedirect("/users/")
	    else:
		return HttpResponse("Some Error has Occured")
    else:
	form = ChangePasswordForm()
    return render_to_response("password.html", {"form":form}, context_instance=RequestContext(request))



###

class TForm(forms.Form):
    file = forms.FileField()



@login_required
def upload(request):
    if slave==True:
	message = "I am slave go to my master on %s" % (master_ip)
	return HttpResponse(message)
    if request.method=="POST":
	form =TForm(request.POST, request.FILES)
	if form.is_valid():
	    if handle_uploaded_file(request.FILES['file']) == True:
		return HttpResponseRedirect('/users/')
	    else:
		return HttpResponse("Make sure the CSV has 5 columns. All correctly filled using text. No special Chars,")
    else:
        form = TForm()
    return render_to_response('upload.html', {'form': form}, context_instance=RequestContext(request))
	    
	    
    
def handle_uploaded_file(f):
    reader = csv.reader(f)
    for row in reader:
	
	if len(row)<5:
	    return False
	else:
	    
	    user=LdapUser()
	    user.username = row[0]
	    if user.username in [u.username for u in LdapUser.objects.all()]:
		user.username =user.username +"_" + str(random.randint(0, 10000))
	    user.first_name =row[1]
	    user.phone = phone ='9888003331'
	    
	    user.last_name = row[2]
	    user.full_name = row[1] +"  " + row[2]
	    user.email =row[3]
	    user.group = base_group
	    user.gecos = user.full_name
	    
	    #return HttpResponse(user.username +" " " " + user.gecos +"  " + str(base_group) + " " + user.gecos)
	    uids =[u.uid for u in LdapUser.objects.all()] 
	    #return HttpResponse(str(uids))
	    if  len(uids)!=0:
		uid_max = max(uids)
	    else:
		uid_max =uid_start 
	    user.uid = uid_max +1
	    #return HttpResponse(str(user.uid))
	    user.home_directory = os.path.join(home_start_path, user.username)
	    user.save()
	    password1= row[4]
	    dn =find_dn(user.username)
	    x= change_p(dn, password1)
	    if slave ==False:
		if len(slave_ips)>0:
		    for ip in slave_ips:
			url ="http://%s:%s/api_users/add/" %(ip, str(port))
			payload ={"secret_key":secret_k, "uid":user.uid, "email":user.email, "first_name":user.first_name,
			"last_name":user.last_name, 
			"username": user.username,
			"password":password1,}
			if phone !=None:
			    payload["phone"] =str(phone)
			requests.post(url,payload)
	    
    return True

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def post_login(request):
    if request.method=="POST":
	users2= LdapUser.objects.all()
	users = [user.username for user in users2]
	username = request.POST.get("username")
	if username in users:
	    pass
	else:
	    if "uid=" in username:
		u=username.replace("uid=", '')
		try:
		    uid =int(u.strip())
		    try:
			ldap =LdapUser.objects.get(uid=uid)
			username =ldap.username
		    except LdapUser.DoesNotExist:
			return HttpResponse("No User")
		except ValueError:
		    return HttpResponse("No User")
	    else:
		return HttpResponse("No User")
	    
	time= request.POST.get("time")
	con_time = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
	try:
	    login =LastLogin.objects.get(user=username)
	    login.time = con_time
	    login.save()
	except LastLogin.DoesNotExist:
	    login = LastLogin()
	    login.user =username
	    login.time = con_time
	    login.save()
	return HttpResponse("OK")

    
@login_required
def last_logins(request):
    logins = LastLogin.objects.all()
    return render_to_response("last_logins.html", {'object_list': logins}, context_instance=RequestContext(request))


@login_required
def inactive_accounts(request):
    days_60 =datetime.datetime.now() -datetime.timedelta(60,0,0)
    logins = LastLogin.objects.filter(time__lte =days_60)
    return render_to_response("in_logins.html", {'object_list': logins}, context_instance=RequestContext(request))
mapped ={1006:1107}

def get_password_time(request, uid):
    try:
	p=PasswordManager.objects.get(user=int(uid))
	days =(datetime.datetime.now() - p.time).days
	if days>45:
	    response_data={}
	    response_data["days"] =str(days)
	    response_data["status"] =1
	else:
	    response_data={}
	    response_data["days"] =str(days)
	    response_data["status"] =0
	return HttpResponse(json.dumps(response_data), content_type="application/json")
    
    except PasswordManager.DoesNotExist:
	response_data={}
	return HttpResponse(json.dumps(response_data), content_type="application/json")
	
    
