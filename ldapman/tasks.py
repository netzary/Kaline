from models import *
from local_ldap import *
from ldap_settings import *
import datetime, time

def task_add_user(first_name, last_name, username, email,  password, uid, phone):
    print "Reached tasks"
    try:
	user = LdapUser.objects.get(uid__exact=int(uid))
    except LdapUser.DoesNotExist:
	user=LdapUser()
    user.first_name = first_name
    user.last_name = last_name
    user.full_name = first_name+ " " + last_name
    user.username =username
    user.email =email
    user.group = 2000
    user.gecos = user.full_name
    if phone !=None:
	user.phone =phone 
    user.home_directory = os.path.join(home_start_path, user.username)
    user.uid =int(uid)
    user.save()
    dn =find_dn(user.username)
    x= change_p(dn, password)
    uid =user.uid

    try:
	pman = PasswordManager.objects.get(user=uid)
	pman.time =datetime.datetime.today()
	pman.save()
	return True
    except PasswordManager.DoesNotExist:
	pman = PasswordManager()
	pman.user =uid
	pman.time =datetime.datetime.today()
	pman.save()
	return True


def task_add_group(name, gid):
    try:
	f=LdapGroup.objects.get(gid__exact=gid)
	print 22
    except LdapGroup.DoesNotExist:
	print 33
	f=LdapGroup()
    f.name = name
    f.gid = int(gid)
    f.save()
	
def task_delete_user(user):
    try:
	u =  LdapUser.objects.get(username__exact = user)
	u.delete()
    except LdapUser.DoesNotExist:
	pass
		
		
def task_delete_group(group):
    group = LdapGroup.objects.get(name__exact = group)

    if len(group.usernames) == 0:
	group.delete()

def task_change_password(user,password):
    print "Kunnas"
    dn =find_dn(user)
    x= change_p(dn, password)
    u =LdapUser.objects.get(username=user)
    uid = u.uid
    print "Kunnas"
    try:
	print "Kunnas"
	pman = PasswordManager.objects.get(user=uid)
	pman.time =datetime.datetime.today()
	pman.save()
    except PasswordManager.DoesNotExist:
	print "Kunnas12"
	pman = PasswordManager()
	pman.user =uid
	pman.time =datetime.datetime.today()
	pman.save()
    
    
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
	    user.home_directory = os.path.join(home_start_path, user.username)
	    user.save()
	    password1= row[4]
	    dn =find_dn(user.username)
	    x= change_p(dn, password1)
	    
    return True

