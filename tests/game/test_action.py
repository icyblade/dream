import pytest


def test_action():
    from dream.game.action import Action

    assert Action('FOLD').action == 0.0
    assert Action('CHECK').action == -1.0
    assert Action('CALL').action == -2.0
    assert Action('ALLIN').action == -3.0
    assert Action('RAISE123').action == 123.0
    assert Action('RAISE 123.1').action == 123.1

    assert repr(Action('FOLD')) == 'fold'
    assert repr(Action('CHECK')) == 'check'
    assert repr(Action('CALL')) == 'call'
    assert repr(Action('ALLIN')) == 'allin'
    assert repr(Action('RAISE123')) == 'raise 123.0'
    assert repr(Action('RAISE 123.1')) == 'raise 123.1'

    with pytest.raises(ValueError):
        Action('RAISE PANTS')

    with pytest.raises(ValueError):
        Action('FLOP THE TABLE')
