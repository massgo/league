# -*- coding: utf-8 -*-
"""Dashboard models."""

from enum import Enum

from league.database import (Column, Model, SurrogatePK, association_proxy, db,
                             func, reference_col, relationship, session)

Color = Enum('Color', 'white black')
Color.white.abbr = 'w'
Color.black.abbr = 'b'


class Player(SurrogatePK, Model):
    """A player."""

    __tablename__ = 'players'

    first_name = Column(db.String(30))
    last_name = Column(db.String(30))
    aga_id = Column(db.Integer, index=True, unique=True)
    aga_rank = Column(db.Integer)

    white_player_games = relationship('WhitePlayerGame', backref='player')
    white_games = association_proxy('white_player_games', 'game')

    black_player_games = relationship('BlackPlayerGame', backref='player')
    black_games = association_proxy('black_player_games', 'game')

    def __init__(self, first_name, last_name, aga_id, aga_rank):
        """Initialize player."""
        self.first_name = first_name
        self.last_name = last_name
        self.aga_id = aga_id
        self.aga_rank = aga_rank

    def __repr__(self):
        """Represent instance as a unique string."""
        return ('<Player({first_name}, {last_name}, {aga_id})>'.
                format(first_name=self.first_name, last_name=self.last_name,
                       aga_id=self.aga_id))

    @property
    def games(self):
        """All games that player has played."""
        return self.black_games + self.white_games

    @property
    def full_name(self):
        """Full player name."""
        return '{0} {1}'.format(self.first_name, self.last_name)

    @classmethod
    def get_by_aga_id(cls, aga_id):
        """Get player by AGA ID."""
        return cls.query.filter_by(aga_id=aga_id)[0]

    @classmethod
    def get_players(cls):
        """Get all players."""
        return cls.query.all()


class Game(SurrogatePK, Model):
    """A game record."""

    __tablename__ = 'games'

    white_player_game = relationship('WhitePlayerGame', backref='game',
                                     cascade='all, delete-orphan',
                                     uselist=False)
    white = association_proxy('white_player_game', 'player',
                              creator=lambda pl: WhitePlayerGame(player=pl))

    black_player_game = relationship('BlackPlayerGame', backref='game',
                                     cascade='all, delete-orphan',
                                     uselist=False)
    black = association_proxy('black_player_game', 'player',
                              creator=lambda pl: BlackPlayerGame(player=pl))

    winner = Column(db.Enum(Color))
    handicap = Column(db.SmallInteger)
    komi = Column(db.SmallInteger)
    season = Column(db.Integer)
    episode = Column(db.Integer)

    db.Index('ix_games_season_episode', 'season', 'episode')

    def __init__(self, white, black, winner, handicap, komi, season, episode):
        """Initialize game."""
        self.white = white
        self.black = black
        self.winner = winner
        self.handicap = handicap
        self.komi = komi
        self.season = season
        self.episode = episode

    def __repr__(self):
        """Represent instance as a unique string."""
        return ('<Game({white!r}, {black!r}, {winner}, {handicap}, {komi})>'.
                format(white=self.white, black=self.black, winner=self.winner,
                       handicap=self.handicap, komi=self.komi))

    @classmethod
    def get_by_season_ep(cls, season, episode):
        """Get games by season and episode."""
        return cls.query.filter_by(season=season, episode=episode)

    @classmethod
    def get_max_season_ep(cls):
        """Get maximum season and episode."""
        max_season, max_episode = session.query(func.max(cls.season),
                                                func.max(cls.episode)).one()

        max_season = 0 if max_season is None else max_season
        max_episode = 0 if max_episode is None else max_episode

        return (max_season, max_episode)

    @property
    def players(self):
        """Get players in game as set."""
        return frozenset((self.white, self.black))


class WhitePlayerGame(Model):
    """A map between players and the games they've played as white."""

    __tablename__ = 'white_player_games'

    player_id = reference_col('players', primary_key=True)
    game_id = reference_col('games', primary_key=True)


class BlackPlayerGame(Model):
    """A map between players and the games they've played as black."""

    __tablename__ = 'black_player_games'

    player_id = reference_col('players', primary_key=True)
    game_id = reference_col('games', primary_key=True)
