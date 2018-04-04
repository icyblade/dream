def test_base_agent():
    from dream.agent import BaseAgent

    agent = BaseAgent()
    assert agent.in_game is None
    assert agent.run() is None
    assert agent.observe() is None
    assert agent.act('SOME_ACTION') is None
