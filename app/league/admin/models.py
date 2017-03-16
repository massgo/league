# -*- coding: utf-8 -*-
"""Admin models."""
import datetime as dt

from flask_login import UserMixin

from league.database import (Column, Model, SurrogatePK, db, reference_col,
                             relationship)
from league.extensions import bcrypt


class ConfigData(SurrogatePK, Model):
    """Configuration data for app extensions."""

    __tablename__ = 'config_data'
    key = Column(db.String(80), unique=True, nullable=False)
    value = Column(db.String(80), nullable=False)

    def __init__(self, key, value, **kwargs):
        """Create instance."""
        db.Model.__init__(self, key=key, value=value, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<ConfigData({key})>'.format(key=self.key)

    @classmethod
    def get_by_key(cls, key):
        """Get ConfigData by key."""
        return cls.query.filter_by(key=key).first()

    @classmethod
    def get_all(cls):
        """Get all ConfigData."""
        return cls.query.all()


class Role(SurrogatePK, Model):
    """A role for a user."""

    __tablename__ = 'roles'
    name = Column(db.String(80), unique=True, nullable=False)
    user_id = reference_col('users', nullable=True)
    user = relationship('User', backref='roles')

    def __init__(self, name, **kwargs):
        """Create instance."""
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Role({name})>'.format(name=self.name)


class User(UserMixin, SurrogatePK, Model):
    """A user of the app."""

    __tablename__ = 'users'
    username = Column(db.String(80), unique=True, nullable=False)
    email = Column(db.String(80), unique=True, nullable=False)
    #: The hashed password
    password = Column(db.Binary(128), nullable=True)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    first_name = Column(db.String(30), nullable=True)
    last_name = Column(db.String(30), nullable=True)
    active = Column(db.Boolean(), default=False)
    is_admin = Column(db.Boolean(), default=False)

    def __init__(self, username, email, password=None, is_admin=False,
                 **kwargs):
        """Create instance."""
        db.Model.__init__(self, username=username, email=email,
                          is_admin=is_admin, **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None

    def set_password(self, password):
        """Set password."""
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        """Check password."""
        return bcrypt.check_password_hash(self.password, value)

    @property
    def full_name(self):
        """Full user name."""
        return '{0} {1}'.format(self.first_name, self.last_name)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<User({username!r})>'.format(username=self.username)

    @classmethod
    def get_by_username(cls, username):
        """Get User by username."""
        return cls.query.filter_by(username=username).first()

    @classmethod
    def get_all(cls):
        """Get all users."""
        return cls.query.all()

    @classmethod
    def delete_by_id(cls, ids):
        """Delete users by id."""
        cls.query.filter(User.id.in_(ids)).delete(synchronize_session=False)
        db.session.commit()
