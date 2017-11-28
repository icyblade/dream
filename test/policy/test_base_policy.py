def test_base_policy():
    from dream.policy import BasePolicy

    policy = BasePolicy()

    assert policy.act(None, None, True) is None
