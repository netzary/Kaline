server = 'ldap://127.0.0.1'

import ldap
l = ldap.initialize(server)
from ldap_settings import *
def getusers():
    try:
	results=l.search_s(base_dn_user, ldap.SCOPE_SUBTREE)
	groups=[results[i][1]['cn'][0] for i in range(0, len(results)-1) if results[i][1].has_key('cn')]

	
	return tuple ([(r,r) for r in groups])
	#dis=[res[i][1]['memberUid'] for i in range(0, len(res)-1) if res[i][1]['cn'][0]=='gn_accounts'][0]
    except ldap.SERVER_DOWN:
	return (("usernotefound", "usernotefound"),)


def get_user_list():
    try:
	results=l.search_s(base_dn_user, ldap.SCOPE_SUBTREE)
	groups=[results[i][1]['uid'][0] for i in range(0, len(results)) if results[i][1].has_key('uid')]

	
	return groups
	#dis=[res[i][1]['memberUid'] for i in range(0, len(res)-1) if res[i][1]['cn'][0]=='gn_accounts'][0]
    except ldap.SERVER_DOWN:
	return ("usernotefound")




def get_groups():
    try:
	results=l.search_s(base_dn_group, ldap.SCOPE_SUBTREE)
	groups=[results[i][1]['cn'][0] for i in range(0, len(results)) if results[i][1].has_key('cn')]
	res=[r for r in results if r[1].has_key('cn')]
	groups=[res[i][1]['cn'][0] for i in range(0, len(res)-1) if res[i][1].has_key('cn')]
	return tuple ([(r,r) for r in groups])
	#dis=[res[i][1]['memberUid'] for i in range(0, len(res)-1) if res[i][1]['cn'][0]=='gn_accounts'][0]
    except ldap.SERVER_DOWN:
	return (("server_not_found", "server_not_found"),)




def get_group_list():
    try:
	results=l.search_s(base_dn_group, ldap.SCOPE_SUBTREE)
	groups=[results[i][1]['cn'][0] for i in range(0, len(results)) if results[i][1].has_key('cn')]
	res=[r for r in results if r[1].has_key('cn')]
	groups=[res[i][1]['cn'][0] for i in range(0, len(res)) if res[i][1].has_key('cn')]
	return groups
	#dis=[res[i][1]['memberUid'] for i in range(0, len(res)-1) if res[i][1]['cn'][0]=='gn_accounts'][0]
    except ldap.SERVER_DOWN:
	return (("server_not_found", "server_not_found"),)




import ldap
import os
import hashlib
import base64
import getpass
import argparse
from time import time
import pprint

def find_dn(user):
    l =ldap.initialize(server)
    results=l.search_s(base_dn_user, ldap.SCOPE_SUBTREE)
    res = [r for r in results if r[1].has_key('uid')]
    try:
	dn=[r[0] for r in res if r[1]['uid'][0] ==user][0]
	return dn
    except IndexError:
	return None
    except KeyError:
	return None


def change_p(dn, password):
    l =ldap.initialize(server)
    
    
    try:
	l.simple_bind_s(admin_dn, admin_pwd)
	
	salt = os.urandom(4)  # random 4-byte binary
	h = hashlib.sha1()
	h.update(password)
	h.update(salt)
	
	userPassword = "{SSHA}" + base64.b64encode(h.digest() + salt)
 
	seconds_per_day = 24 * 60 * 60
	shadowLastChange = int( time() / seconds_per_day )
 
	attrs = [(ldap.MOD_REPLACE, 'userPassword', userPassword )]
	l.modify_s(dn, attrs)
	return 1
    
    
    except  ldap.LDAPError, e:
	return 0
    
    
