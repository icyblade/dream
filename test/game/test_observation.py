import pytest


def test_observation():
    with pytest.raises(NotImplementedError):
        from dream.game.observation import Observation
