# LDAP alias model object
from app import app
from app.models import LDAPAlias

ldap_server = app.config.get('LDAP_HOST')
ldap_user = app.config.get('LDAP_BIND_USER_DN')
ldap_password = app.config.get('LDAP_BIND_USER_PASSWORD')

LDAP = LDAPAlias(ldap_server, ldap_user, ldap_password)

from flask import Blueprint
alias = Blueprint('alias', __name__, template_folder='templates')

from . import views