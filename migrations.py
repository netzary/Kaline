from ldap_settings import *
import ldap
l = ldap.initialize(server)

import os
import sys, datetime, subprocess
from django.core.management import setup_environ
import settings, csv
from django.utils.encoding import DjangoUnicodeDecodeError
setup_environ(settings)
from ldapman.models import *
def get_user_list():
    try:
	results=l.search_s(base_dn_user, ldap.SCOPE_SUBTREE)
	groups=[results[i][1]['uid'][0] for i in range(0, len(results)) if results[i][1].has_key('uid')]

	
	return groups
	#dis=[res[i][1]['memberUid'] for i in range(0, len(res)-1) if res[i][1]['cn'][0]=='gn_accounts'][0]
    except ldap.SERVER_DOWN:
	return (("usernotefound", "usernotefound"),)
	


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


def migrate_users():
    all_users = get_user_list()
    current = [u.uid for u in LdapUser.objects.all()]
    for user in all_users:
	if user not in current:
	    try:
		results=l.search_s(base_dn_user, ldap.SCOPE_SUBTREE)
		res =[r[1] for r in results if r[1].has_key('uid')]
		dic = [r for r in res if r['uid'][0]== user][0]
		l_user=LdapUser()
		
		if dic.has_key('uid'):
		    cn = dic['uid'][0]
		    l_user.username =cn
		else: 
		    pass
		if dic.has_key('cn'):
		    cn = dic['cn'][0]
		    l_user.full_name = l_user.first_name =l_user.last_name =cn
		else: 
		    pass
		if dic.has_key('gecos'):
		    cn = dic['gecos'][0]
		    l_user.gecos =cn
		else: 
		    pass
		
		if dic.has_key('uidNumber'):
		    cn = int(dic['uidNumber'][0])
		    l_user.uid =cn
		else: 
		    pass
		
		if dic.has_key('gidNumber'):
		    cn = int(dic['gidNumber'][0])
		    l_user.group =cn
		else: 
		    pass
		if dic.has_key('homeDirectory'):
		    cn = dic['homeDirectory'][0]
		    l_user.home_directory =cn
		else: 
		    pass
		if dic.has_key('sn'):
		    cn = dic['sn'][0]
		    l_user.last_name =cn
		else: 
		    pass
		
		if dic.has_key('givenName'):
		    cn = dic['givenName'][0]
		    l_user.first_name =cn
		else: 
		    pass
		if dic.has_key('mail'):
		    cn = dic['mail'][0]
		    l_user.email =cn
		else: 
		    l_user.email ="not@not.com"
		l_user.save()
	    except KeyError:
		pass
	    except IndexError:
		pass
	    except ValueError:
		pass

if __name__=="__main__":
    migrate_users()
