# -*- coding: utf-8 -*-
"""Defines fixtures available to all API tests."""

import pytest

from .factories import GameFactory, PlayerFactory


@pytest.fixture
def players(db):
    """Some players for the tests."""
    players = [PlayerFactory(), PlayerFactory()]
    db.session.commit()
    return players


@pytest.fixture
def games(db):
    """Some games for the tests."""
    games = [GameFactory(), GameFactory()]
    db.session.commit()
    return games


@pytest.fixture
def season_choices():
    """Season choices to use when testing game create form."""
    return [(s, s) for s in range(0, 3)]


@pytest.fixture
def episode_choices():
    """Episode choices to use when testing game create form."""
    return [(e, e) for e in range(0, 2)]
