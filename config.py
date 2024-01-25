THREADS_PER_PAGE = 4

WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

#LDAP_HOST = 'localhost'
LDAP_HOST = 'aux.s7.ru'
LDAP_BASE_DN = 'ou=system,dc=s7,dc=ru'
LDAP_USER_DN = 'ou=People'
LDAP_SEARCH_FOR_GROUPS = False
LDAP_BIND_USER_DN = 'cn=pybot,dc=s7,dc=ru'
LDAP_BIND_USER_PASSWORD = 'Tsk12exb'
