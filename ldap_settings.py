
import ldap
ldap_dic={
        'ENGINE': 'ldapdb.backends.ldap',
        'NAME': 'ldap://127.0.0.1',
        'USER': 'cn=admin,dc=polariscs,dc=local',
        'PASSWORD': 'Welcome03#',
    }
base_dn_user = "ou=People,dc=polariscs,dc=local"
base_dn_group = "ou=Groups,dc=polariscs,dc=local"
uid_start = 1100
gid_start =2000
base_group = 2000
home_start_path ="/home" # Start  path of Home Directory 
server = 'ldap://127.0.0.1'
admin_dn ='cn=admin,dc=polariscs,dc=local'
admin_pwd = 'Welcome03#'
