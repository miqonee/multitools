from ldap3 import MODIFY_REPLACE, LEVEL


class AliasObject:
    def __init__(self, name, ldap_alias):
        self.key = name
        self.ldapconn = ldap_alias
        with self.ldapconn.connect_ldap() as conn:
            if conn.search(self.ldapconn.search_base,
                           self.ldapconn.s_f(name), search_scope=LEVEL,
                           attributes=['description', 'sendmailMTAAliasValue']):
                self.dn = conn.entries[0].entry_dn
                self.description = conn.entries[0].description.values
                self.values = conn.entries[0].sendmailMTAAliasValue.values
            else:
                self.dn = ldap_alias.edn(name)
                self.values = ['noreply']
            if conn.search('ou=mail,dc=s7,dc=ru',
                           '(mailRoutingAddress={0}@localhost)'.format(name)):
                self.honesty = False
            else:
                self.honesty = True

    def clean(self):
        self.description = [e for e in self.description if e != '']
        self.values = [e for e in self.values if e != '']

    def add2ldap(self):
        with self.ldapconn.connect_ldap() as conn:
            if self.honesty:
                object_class = ['sendmailMTAAliasObject', 'inetLocalMailRecipient']
                attributes = {'sendmailMTAAliasValue': self.values,
                              'sendmailMTAAliasGrouping': 'aliases',
                              'sendmailMTACluster': 'servers',
                              'sendmailMTAHost': 'localhost',
                              'mailHost': 'localhost',
                              'mailLocalAddress': '{0}@s7.ru'.format(self.key),
                              'mailRoutingAddress': '{0}@localhost'.format(self.key)}
            else:
                object_class = ['sendmailMTAAliasObject']
                attributes = {'sendmailMTAAliasValue': [self.key] + self.values,
                              'sendmailMTAAliasGrouping': 'aliases',
                              'sendmailMTACluster': 'servers',
                              'sendmailMTAHost': 'localhost'}
            conn.add(self.dn, object_class, attributes)
        return conn.result['description']

    def change(self):
        with self.ldapconn.connect_ldap() as conn:
            result = conn.modify(self.dn,
                                 {'sendmailMTAAliasValue': [(MODIFY_REPLACE, self.values)],
                                  'description': [(MODIFY_REPLACE, self.description)]}
                                 )
        return result
