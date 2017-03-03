# -*- coding: utf-8 -*-
"""Dashboard models."""

import datetime as dt
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

    def latest_season(self):
        """Get latest season player has played in."""
        return sorted([game.season for game in self.games])[-1]

    def season_stats(self, season=None):
        """Get player statistics for a season."""
        if season is None:
            season = Game.latest_season_episode()[0]

        wins, losses = 0, 0
        for game in ([game for game in self.games if game.season == season]):
            if ((game.winner == Color.white and game.white == self) or
                    (game.winner == Color.black and game.black == self)):
                wins += 1
            else:
                losses += 1

        return {'wins': wins, 'losses': losses}

    def latest_season_episode(self):
        """Get latest season and episode player has played in."""
        games = self.games
        if len(games) > 0:
            return sorted([(game.season, game.episode)
                           for game in games])[-1]
        else:
            return (0, 0)

    def episode_stats(self, season_episode=None):
        """Get player statistics for an episode."""
        latest_season_episode = Game.latest_season_episode()
        if season_episode is None:
            season_episode = latest_season_episode
        wins, losses = 0, 0

        for game in ([game for game in self.games
                      if game.season == season_episode[0] and
                      game.episode == season_episode[1]]):
            if ((game.winner == Color.white and game.white == self) or
                    (game.winner == Color.black and game.black == self)):
                wins += 1
            else:
                losses += 1

        return {'wins': wins, 'losses': losses}

    def league_stats(self):
        """Get player statistics for the whole league."""
        wins, losses = 0, 0
        for game in self.games:
            if ((game.winner == Color.white and game.white == self) or
                    (game.winner == Color.black and game.black == self)):
                wins += 1
            else:
                losses += 1

        return {'wins': wins, 'losses': losses}


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

    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    played_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    last_modified_at = Column(db.DateTime, nullable=False,
                              default=dt.datetime.utcnow)

    db.Index('ix_games_season_episode', 'season', 'episode')

    def __init__(self, white, black, winner, handicap, komi, season, episode,
                 created_at=None, played_at=None, last_modified_at=None):
        """Initialize game."""
        self.white = white
        self.black = black
        self.winner = winner
        self.handicap = handicap
        self.komi = komi
        self.season = season
        self.episode = episode
        self.created_at = created_at
        self.played_at = played_at
        self.last_modified_at = last_modified_at

    def __repr__(self):
        """Represent instance as a unique string."""
        return ('<Game({white!r}, {black!r}, {winner}, {handicap}, {komi})>'.
                format(white=self.white, black=self.black, winner=self.winner,
                       handicap=self.handicap, komi=self.komi))

    def to_dict(self):
        """Return game as dictionary."""
        return {
            'game_id': self.id,
            'white_id': self.white.id,
            'black_id': self.black.id,
            'winner': self.winner.name,
            'handicap': self.handicap,
            'komi': self.komi,
            'season': self.season,
            'episode': self.episode,
            'created_at': str(self.created_at),
            'played_at': str(self.played_at),
            'last_modified_at': str(self.last_modified_at)
        }

    def update(self, **kwargs):
        """Override update method to reset last_modified_at."""
        self.last_modified_at = dt.datetime.utcnow()
        super().update(**kwargs)

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

    @classmethod
    def latest_season_episode(cls):
        """Get latest episode and season."""
        games = cls.query.all()
        if len(games) > 0:
            return sorted([(game.season, game.episode) for game in games])[-1]
        else:
            return (0, 0)

    @classmethod
    def episode_stats(cls, episode=None, season=None, num_players=5):
        """Get statistics for an episode."""
        latest_season_episode = cls.latest_season_episode()
        if episode is None:
            episode = latest_season_episode[1]
        if season is None:
            season = latest_season_episode[0]
        wins, games_played, stones_given = {}, {}, {}
        games = [game for game in cls.query.all()
                 if game.season == season and
                 game.episode == episode]
        for game in games:
            if game.winner is Color.white:
                wins[game.white.id] = wins.get(game.white.id, 0) + 1
                stones_given[game.white.id] = stones_given.get(game.white.id, 0)
                + (game.white.handicap)
            else:
                wins[game.black.id] = wins.get(game.black.id, 0) + 1
            games_played[game.white.id] = games_played.get(game.white.id, 0) + 1
            games_played[game.black.id] = games_played.get(game.black.id, 0) + 1

        wins_list = enumerate(sorted(
            [(Player.get_by_id(player_id), player_wins)
             for player_id, player_wins in wins.items()],
            key=lambda stat: stat[1],
            reverse=True
        )[0:num_players])

        games_played_list = enumerate(sorted(
            [(Player.get_by_id(player_id), player_games_played)
             for player_id, player_games_played in games_played.items()],
            key=lambda stat: stat[1],
            reverse=True
        )[0:num_players])

        stones_given_list = enumerate(sorted(
            [(Player.get_by_id(player_id), player_stones_given)
             for player_id, player_stones_given in stones_given.items()],
            key=lambda stat: stat[1],
            reverse=True
        )[0:num_players])

        return {'wins': wins_list,
                'games_played': games_played_list,
                'stones_given': stones_given_list}


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
