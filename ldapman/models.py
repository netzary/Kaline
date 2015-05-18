# -*- coding: utf-8 -*-
#
# django-ldapdb
# Copyright (c) 2009-2011, Bolloré telecom
# All rights reserved.
#
# See AUTHORS file for a full list of contributors.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
#     1. Redistributions of source code must retain the above copyright notice,
#        this list of conditions and the following disclaimer.
#
#     2. Redistributions in binary form must reproduce the above copyright
#        notice, this list of conditions and the following disclaimer in the
#        documentation and/or other materials provided with the distribution.
#
#     3. Neither the name of Bolloré telecom nor the names of its contributors
#        may be used to endorse or promote products derived from this software
#        without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

from ldapdb.models.fields import CharField, ImageField, IntegerField, ListField
import ldapdb.models
from ldap_settings import *

class LdapUser(ldapdb.models.Model):
    """
    Class for representing an LDAP user entry.
    """
    # LDAP meta-data
    base_dn = base_dn_user
    object_classes = ['posixAccount', 'shadowAccount', 'inetOrgPerson']

    # inetOrgPerson
    first_name = CharField(db_column='givenName')
    last_name = CharField(db_column='sn')
    full_name = CharField(db_column='cn')
    email = CharField(db_column='mail')
    phone = CharField(db_column='telephoneNumber', blank=True)
    mobile_phone = CharField(db_column='mobile', blank=True)
    photo = ImageField(db_column='jpegPhoto')

    # posixAccount
    uid = IntegerField(db_column='uidNumber', unique=True)
    group = IntegerField(db_column='gidNumber')
    gecos =  CharField(db_column='gecos')
    home_directory = CharField(db_column='homeDirectory')
    login_shell = CharField(db_column='loginShell', default='/bin/bash')
    username = CharField(db_column='uid', primary_key=True)
    password = CharField(db_column='userPassword')

    def __str__(self):
        return self.username

    def __unicode__(self):
        return self.full_name
    class Meta:
	ordering =('username',)
	
	
	
class LdapGroup(ldapdb.models.Model):
    """
    Class for representing an LDAP group entry.
    """
    # LDAP meta-data
    base_dn = base_dn_group
    object_classes = ['posixGroup']

    # posixGroup attributes
    gid = IntegerField(db_column='gidNumber', unique=True)
    name = CharField(db_column='cn', max_length=200, primary_key=True)
    usernames = ListField(db_column='memberUid')

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    def get_usernames(self):
        return ", ". join (self.usernames)


from django.db import models
import datetime
class PasswordManager(models.Model):
    user = models.IntegerField(unique=True)
    time = models.DateTimeField()
    
    def __unicode__(self):
	return str(self.id)

class LastLogin(models.Model):
    user= models.CharField(max_length=100, unique=True)
    time = models.DateTimeField()
    def __unicode__(self):
	return str(self.user)

