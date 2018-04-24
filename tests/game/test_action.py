import pytest


def test_action():
    from dream.game.action import Action, BaseAction, get_raise_strength

    assert repr(Action('Fold')) == 'FOLD'
    assert repr(Action('CHECK')) == 'CHECK'
    assert repr(Action('call')) == 'CALL'
    assert repr(Action('aLLiN')) == 'ALLIN'
    assert repr(Action('RAISE123')) == 'RAISE 123.0'
    assert repr(Action('RAISE 123.1')) == 'RAISE 123.1'
    assert repr(Action('RAISE 123.1', raise_from=100)) == 'RAISE 123.1 from 100.0'

    assert Action('CALL').raise_to is None
    assert Action('RAISE 123').raise_to == 123

    assert Action(BaseAction('CALL')) == Action('call')

    with pytest.raises(ValueError):
        Action(BaseAction('Raise'))

    action = Action('RAISE 123')
    action.raise_from = 100
    assert action.raise_from == 100
    assert action.raise_to == 123
    assert action.raise_mult == 1.23

    action = Action('RAISE 123', raise_from=100)
    assert action.raise_from == 100
    assert action.raise_to == 123
    assert action.raise_mult == 1.23
    assert action.minimum_raise == 23

    action = Action('RAISE 123')
    action.raise_from = '100'
    assert action.raise_mult == 1.23

    action = Action('CALL')
    with pytest.raises(Exception):
        action.raise_from = 100
    assert action.raise_from is None

    action = Action('RAISE 123', raise_from=100)
    previous_action = Action('RAISE 100', raise_from=90)
    assert get_raise_strength(action) == 0.23
    assert get_raise_strength(action, previous_action) == 2.3
