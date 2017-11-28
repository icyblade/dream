import pytest


def test_action():
    from dream.game.action import Action

    assert Action('FOLD').action == -1.0
    assert Action('CALL').action == 0.0
    assert Action('ALLIN').action == float('inf')
    assert Action('RAISE123').action == 123.0
    assert Action('RAISE 123.1').action == 123.1

    assert repr(Action('FOLD')) == '-1.0'
    assert repr(Action('CALL')) == '0.0'
    assert repr(Action('ALLIN').action) == 'inf'
    assert repr(Action('RAISE123')) == '123.0'
    assert repr(Action('RAISE 123.1')) == '123.1'

    with pytest.raises(ValueError):
        Action('RAISE PANTS')

    with pytest.raises(ValueError):
        Action('FLOP THE TABLE')
