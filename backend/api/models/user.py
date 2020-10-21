# from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from sqlalchemy import *
from datetime import datetime

from . import Base


class User(Base):
    username = Column(String, index=True, unique=True)
    name = Column(String)
    title = Column(String)
    department = Column(String)
    company = Column(String)
    is_admin = Column(Boolean, default=False)
    first_seen = Column(DateTime, default=datetime.utcnow)
    last_seen = Column(DateTime, default=datetime.utcnow)

    # def generate_auth_token(self, expiration=config.TOKEN_TTL):
    #     s = Serializer(config.SECRET_KEY, expires_in=expiration)
    #     return s.dumps({'id': self.id})
    #
    # @staticmethod
    # def verify_auth_token(token):
    #     s = Serializer(config.SECRET_KEY)
    #
    #     try:
    #         data = s.loads(token)
    #     except SignatureExpired:
    #         return None  # valid token, but expired
    #     except BadSignature:
    #         return None  # invalid token
    #
    #     user = User.query.get(data['id'])
    #
    #     user.update(last_seen=datetime.utcnow())
    #     db.session.commit()
    #
    #     return user
    #
    # def __repr__(self):
    #     return '<User {}>'.format(self.username)
