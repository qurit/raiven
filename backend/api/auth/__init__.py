from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

from flask_httpauth import HTTPTokenAuth

from api import config

from .ldap import LDAPManager

token_auth = HTTPTokenAuth()
ldap = LDAPManager()


@token_auth.verify_token
def verify_token(token):
    s = Serializer(config.SECRET_KEY)

    try:
        data = s.loads(token)
    except SignatureExpired:
        return None  # valid token, but expired
    except BadSignature:
        return None  # invalid token
    else:
        return 'OK'


def verify_password(username, password):
    if username and username.endswith('@bccrc.ca'):
        username = username.replace('@bccrc.ca', '')

    if not config.AUTH_ENABLED:
        user = {"name": 'test'}
    else:
        user = ldap.authenticate(username, password)

    return user
