def test_reward():
    from dream.game.reward import Reward

    assert isinstance(Reward(1), float)
