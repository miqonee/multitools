# LDAP alias model object
from app import app
from app.models import LDAPProxy

ldap_server = app.config.get('LDAP_HOST')
ldap_user = app.config.get('LDAP_BIND_USER_DN')
ldap_password = app.config.get('LDAP_BIND_USER_PASSWORD')

ldap_proxy = LDAPProxy(ldap_server, ldap_user, ldap_password)

from flask import Blueprint
proxy = Blueprint('proxy', __name__, template_folder='templates')

from . import views