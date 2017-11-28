def test_recv():
    from dream.agent.apple_apricot import Agent

    Agent('test', 'tcp://127.0.0.1:10000', 'tcp://127.0.0.1:10001')
