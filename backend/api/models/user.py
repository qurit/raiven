from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from passlib.hash import pbkdf2_sha256

from sqlalchemy import *
from sqlalchemy.orm import relationship
from datetime import datetime

from . import Base
from api import config


class User(Base):
    username = Column(String, index=True, unique=True)
    name = Column(String)
    is_admin = Column(Boolean, default=False)
    first_seen = Column(DateTime, default=datetime.utcnow)
    last_seen = Column(DateTime, default=datetime.utcnow)

    ldap_user = relationship("UserLDAP", backref='user', uselist=False)
    local_user = relationship("UserLocal", backref='user', uselist=False)

    def generate_token(self, expiration=config.TOKEN_TTL):
        s = Serializer(config.SECRET_KEY, expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_token(token, db):
        s = Serializer(config.SECRET_KEY)

        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token

        user = User.query(db).get(data['id'])
        user.last_seen = datetime.utcnow()
        user.save(db)
        return user


class UserLDAP(Base):
    id = Column(ForeignKey("user.id", ondelete="CASCADE"),  primary_key=True)
    title = Column(String)
    department = Column(String)
    company = Column(String)

    def verify_password(self, password):
        pass


class UserLocal(Base):
    id = Column(ForeignKey("user.id", ondelete="CASCADE"), primary_key=True)
    password = Column(String)

    def verify_password(self, password):
        return pbkdf2_sha256.verify(password, self.password)

    def save(self, *args, **kwargs):
        self.password = pbkdf2_sha256.hash(self.password)
        return super().save(*args, **kwargs)







