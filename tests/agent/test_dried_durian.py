middleware_send_true_message = [
    {
        'RQ': {
            'action': 'PLAYERACTION',
            'data': {
                'playerAction': {
                    'boardCards': '',
                    'log': [
                        'PokerStars Zoom Hand #189:  Hold\'em No Limit ($2/$4) - 2018/01/31 17:52:09 ET',
                        'Table \'2_1\' 9-max Seat #1 is the button',
                        'Seat 1: Test_006 ($1986 in chips)',
                        'Seat 5: AI_005 ($2008 in chips)',
                        'Test_006: posts small blind $2',
                        'AI_005: posts big blind $4',
                        '*** HOLE CARDS ***',
                        'Dealt to bmlm [4h Qd]',
                        'AI_005: checks',
                        'Test_006: folds',
                        '*** SUMMARY ***',
                        'Total pot $6 | Rake $0',
                        'Board []'
                    ],
                    'newCards': '',
                    'player': {
                        'AIID': '2156',
                        'card': '4h Qd',
                        'chips': '2008',
                        'position': '4',
                        'userID': '2400'
                    },
                    'pots': [{
                        'pot': '0'
                    }],
                    'round': 'PREFLOP'
                }
            },
            'requestID': '15',
            'timeStamp': '2018-01-31 17:52:29',
            'token': '869492cc3d74d5bc26f0c9633c3edafb'
        }
    },
    {
        'RQ': {
            'token': '869492cc3d74d5bc26f0c9633c3edafb',
            'requestID': '15',
            'action': 'DELETE',
        }
    }
]

middleware_recv_true_message = [
    {
        'RS': {
            'data': {
                'playerAction': {
                    'action': 'raise 11'
                }
            },
            'requestID': '15',
            'token': '869492cc3d74d5bc26f0c9633c3edafb'
        }
    },
    {
        'RS': {
            'errcode': 0,
            'errmsg': 'Agent exits due to DELETE command.'
        }
    },
]

ai_true_message = [
    'Agent DriedDurian started, binding at tcp://*:41488.',
    'PLAYERACTION',
    'Acting action: raise',
    'raise',
    'DELETE',
    "'errcode': 0",
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

    from dream.agent.dried_durian import Agent

    agent = Agent('DriedDurian', 41488, level=logging.DEBUG)
    agent.run()

    out, err = capsys.readouterr()
    return_value.append(err)


def test_dried_durian(capsys):
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
