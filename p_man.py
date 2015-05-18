from ldap_settings import *


import os
import sys, datetime, subprocess
from django.core.management import setup_environ
import settings, csv
from django.utils.encoding import DjangoUnicodeDecodeError
setup_environ(settings)
from ldapman.models import *

def cross_create():
    a=LdapUser.objects.all()
    for i in a:
	try:
	    p=PasswordManager.objects.get(user=i.uid)
	except PasswordManager.DoesNotExist:
	    p =PasswordManager()
	    p.user =i.uid
	    p = datetime.datetime(2015,1,16,0,4,5)
	    p.save()

