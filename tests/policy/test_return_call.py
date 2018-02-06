def test_return_call():
    from dream.policy.return_call import ReturnCall
    from dream.game.action import Action

    policy = ReturnCall()

    assert isinstance(policy.act(None, None, False), Action)
    assert repr(policy.act(None, None, False)) == 'call'
