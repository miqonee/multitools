from flask_login import UserMixin
from ldap3 import Server, Connection, MODIFY_ADD, MODIFY_DELETE, MODIFY_REPLACE, BASE, LEVEL


class User(UserMixin):
    def __init__(self, dn, username, data):
        self.dn = dn
        self.username = username
        self.data = data

    def __repr__(self):
        return self.dn

    def get_id(self):
        return self.dn


class LDAPAlias:
    """Object for alias management"""

    def __init__(self, host, binddn, bindpw):
        self.server_uri = 'ldaps://' + host
        self.server = Server(self.server_uri)
        self.user = binddn
        self.password = bindpw
        self.search_base = 'ou=aliases,ou=sendmail,ou=mail,dc=s7,dc=ru'

    def connect_ldap(self):
        return Connection(self.server, self.user, self.password, auto_bind=True)

    @staticmethod
    def s_f(expr):
        return '(sendmailMTAKey=' + expr + ')'

    @staticmethod
    def edn(expr):
        return 'sendmailMTAKey=' + expr + ',ou=aliases,ou=sendmail,ou=mail,dc=s7,dc=ru'

    def find_aliases(self, fltr='ldap*'):
        with self.connect_ldap() as conn:
            # search for expression
            conn.search(self.search_base, self.s_f(fltr), search_scope=LEVEL,
                        attributes='sendmailMTAKey')

            # return list of keys for found aliases
            return sorted([entry.sendmailMTAKey.value for entry in conn.entries])

    def check_if_alias(self, conn, name):
        return conn.search(self.search_base, self.s_f(name), search_scope=LEVEL)

    def alias_values(self, alias):
        with self.connect_ldap() as conn:
            # get all alias values
            if conn.search(self.edn(alias), self.s_f(alias), search_scope=BASE,
                           attributes=['description', 'sendmailMTAAliasValue']):
                desc = conn.entries[0].description.value
                result = conn.entries[0].sendmailMTAAliasValue.value

                # make list even for single value
                if isinstance(desc, str):
                    desc = [desc]
                if isinstance(result, str):
                    result = [result]

                # create dict, marking aliases with "True"
                resdict = {e: self.check_if_alias(conn, e) for e in result}

                # if alias has same name as mailbox, mark it
                if alias in resdict:
                    resdict[alias] = False
                return desc, resdict
            else:
                return False, False

    def modify_alias_value(self, option, key, value):
        with self.connect_ldap() as conn:
            act = {
                'add': MODIFY_ADD, 'delete': MODIFY_DELETE
            }
            result = conn.modify(self.edn(key),
                                 {'sendmailMTAAliasValue': [(act[option], [value])]})
            return result


class LDAPProxy:
    """Object for proxy management"""

    def __init__(self, host, binddn, bindpw):
        self.server_uri = 'ldaps://' + host
        self.server = Server(self.server_uri)
        self.user = binddn
        self.password = bindpw
        self.search_base = 'ou=proxy,dc=s7,dc=ru'

    def connect_ldap(self):
        return Connection(self.server, self.user, self.password, auto_bind=True)

    def find_accounts(self, attr='uid', fltr='ldap*'):
        with self.connect_ldap() as conn:
            # search for expression
            conn.search(self.search_base, '({0}={1})'.format(attr, fltr),
                        attributes=['uid', 'cn'])
            return [{'dn': e.entry_dn, 'uid': e.uid.value, 'cn': e.cn.value} for e in conn.entries]

    def account_values(self, dn):
        with self.connect_ldap() as conn:
            # get important attributes
            if conn.search(dn, '(objectClass=s7custom)',
                           attributes=['cn', 'proxySize', 'proxyTempBlock', 'proxyTempNoBlock']):
                return conn.entries[0].entry_attributes_as_dict
            else:
                return False

    def unlim_account(self, dn, value):
        with self.connect_ldap() as conn:
            result = conn.modify(dn, {'proxyTempNoBlock': [(MODIFY_REPLACE, [value])]})
            return result

    def change_limit(self, dn, value):
        with self.connect_ldap() as conn:
            result = conn.modify(dn, {'proxySize': [(MODIFY_REPLACE, [value])]})
            return result
