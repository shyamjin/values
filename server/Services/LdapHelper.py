import ldap
from DBUtil import Config
from settings import mongodb


db = mongodb
configDb = Config.Config(db)

def get_user(username, password):
    auth_service_settings = configDb.getConfigByName('AuthService')
    ldap_server = auth_service_settings.get("ldap_server")
    email = username + auth_service_settings.get("email_domain")
    try:
        connect = ldap.initialize(ldap_server)
        connect.protocol_version = 3
        connect.set_option(ldap.OPT_REFERRALS, 0)
        connect.simple_bind_s(email, password)
        base_dn = auth_service_settings.get("ldap_base_dn")
        query = "(&(objectCategory=user)(sAMAccountName=" + username + "))"
        results = connect.search_s(base_dn, ldap.SCOPE_SUBTREE, query)
        if results:
            return results[0][1]
        else:
            return None
    except ldap.LDAPError:
        return None
