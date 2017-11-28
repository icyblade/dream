def test_base_agent():
    from dream.agent import BaseAgent

    agent = BaseAgent()
    agent.run()
    agent.observe()
    agent.act(None)
    assert agent.in_game is None
