middleware_send_true_message = [
    {
        "RQ": {
            "timeStamp": "2016-06-29 15:39:44",
            "token": "a7d24ed97a089280c9c1d4835fda05b6",
            "requestID": "00000",
            "action": "PLAYERACTION",
            "data": {
                "playerAction": {
                    "pots": {"pot": "999"},
                    "round": "PREFLOP",
                    "boardCards": "AH KC TS",
                    "newCards": "9S",
                    "player": {
                        "userID": "111",
                        "AIID": "0",
                        "position": "6",
                        "card": "AH KC TS",
                        "action": "fold 0",
                        "chips": "20"
                    }
                }
            }
        }
    },
    {
        "RQ": {
            "token": "a7d24ed97a089280c9c1d4835fda05b6",
            "requestID": "00000",
            "action": "DELETE",
        }
    }
]

middleware_recv_true_message = [
    {
        'RS': {
            'data': {
                'playerAction': {
                    'action': 'call'
                }
            },
            'requestID': '00000',
            'token': 'a7d24ed97a089280c9c1d4835fda05b6'
        }
    },
    {
        'RS': {
            'errcode': 1
        }
    },
]

ai_true_message = [
    'Agent BitterBanana started, binding at tcp://*:41488.',
    'PLAYERACTION',
    'Acting action: call.',
    'call',
    'DELETE',
    "{'errcode': 1}",
]

assert len(middleware_send_true_message) == len(middleware_recv_true_message)


def middleware(ip='127.0.0.1'):
    from time import sleep

    import zmq

    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect(f'tcp://{ip}:41488')
    sleep(0.5)  # wait for binding

    for i in range(len(middleware_send_true_message)):
        socket.send_json(middleware_send_true_message[i])
        sleep(0.1)
        assert socket.recv_json() == middleware_recv_true_message[i]
        sleep(0.1)


def ai(capsys, return_value):
    import logging

    from dream.agent.bitter_banana import Agent

    agent = Agent('BitterBanana', 41488, level=logging.DEBUG)
    agent.run()

    out, err = capsys.readouterr()
    return_value.append(err)


def test_bitter_banana(capsys):
    from time import sleep
    from threading import Thread

    ai_return_value = []

    threads = [
        Thread(target=ai, args=(capsys, ai_return_value)),
        Thread(target=middleware),
    ]

    for i in threads:
        i.start()
        sleep(0.1)
    for i in threads:
        i.join()

    assert len(ai_true_message) == len(ai_return_value[0].splitlines())

    for index, pattern in enumerate(ai_true_message):
        assert ai_return_value[0].splitlines()[index].find(pattern) != -1
