# -*- coding: utf-8 -*-
"""API factories."""
from factory import Sequence, SubFactory

from league.models import Color, Game, Player

from ..factories import BaseFactory


class PlayerFactory(BaseFactory):
    """Player factory."""

    first_name = Sequence(lambda n: 'first{0}'.format(n))
    last_name = Sequence(lambda n: 'last{0}'.format(n))
    aga_id = Sequence(lambda n: n + 1000)
    aga_rank = Sequence(lambda n: (n % 9) + 1)

    class Meta:
        """Factory configuration."""

        model = Player


class GameFactory(BaseFactory):
    """Game factory."""

    white = SubFactory(PlayerFactory)
    black = SubFactory(PlayerFactory)
    winner = Color.white
    handicap = 0
    komi = 7
    season = 1
    episode = 1
    created_at = None

    class Meta:
        """Factory configuration."""

        model = Game
