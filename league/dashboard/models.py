# -*- coding: utf-8 -*-
"""Dashboard models."""
from league.database import Column, Model, SurrogatePK, db, reference_col, relationship


class Color(db.Enum):
    """Player color enum."""

    white = 'white'
    black = 'black'


class Game(SurrogatePK, Model):
    """A game record."""

    __tablename__ = 'games'

    white_id = reference_col('players')
    white = relationship('Player', backref='games')

    black_id = reference_col('players')
    black = relationship('Player', backref='games')

    winner = Column(db.Enum(Color))
    handicap = Column(db.SmallInteger)
    komi = Column(db.SmallInteger)


class Player(SurrogatePK, Model):
    """A player."""

    __tablename__ = 'players'

    first_name = Column(db.String(30))
    last_name = Column(db.String(30))
    aga_id = Column(db.Integer)
    rank = Column(db.Integer)

    @property
    def full_name(self):
        """Full player name."""
        return '{0} {1}'.format(self.first_name, self.last_name)
