import pytest


def test_action():
    from dream.game.action import Action, BaseAction

    assert repr(Action('Fold')) == 'FOLD'
    assert repr(Action('CHECK')) == 'CHECK'
    assert repr(Action('call')) == 'CALL'
    assert repr(Action('aLLiN')) == 'ALLIN'
    assert repr(Action('RAISE123')) == 'RAISE 123.0'
    assert repr(Action('RAISE 123.1')) == 'RAISE 123.1'

    assert Action('CALL').get_raise_value() is None
    assert Action('RAISE 123').get_raise_value() == 123

    assert Action(BaseAction('CALL')) == Action('call')

    with pytest.raises(ValueError):
        Action(BaseAction('Raise'))
