import os


upstream_send_message = [
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
                    'pots': {
                        'pot': '0'
                    },
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

upstream_recv_message = [
    {
        'RS': {
            'data': {
                'playerAction': {
                    'action': 'RAISE 77.19834978068214'
                }
            },
            'requestID': '15',
            'token': '869492cc3d74d5bc26f0c9633c3edafb'
        }
    },
    {
        'RS': {
            'errcode': 0,
            'errmsg': 'Agent exits due to DELETE command'
        }
    },
]

ai_message = [
    'Agent TestAgent started, binding at tcp://*:48546',
    "Receiving message: {'RQ': {'action': 'PLAYERACTION',",
    'Acting action:',
    (
        "Sending message: {'RS': {'token': '869492cc3d74d5bc26f0c9633c3edafb', 'requestID': '15', "
        "'data': {'playerAction': {'action': 'RAISE 77.19834978068214'}}}}"
    ),
    "Receiving message: {'RQ': {'token': '869492cc3d74d5bc26f0c9633c3edafb', 'requestID': '15', 'action': 'DELETE'}}",
    'SystemExit captured: Agent exits due to DELETE command',
    "Sending exception: {'RS': {'errcode': 0, 'errmsg': 'Agent exits due to DELETE command'}}",
]

assert len(upstream_send_message) == len(upstream_recv_message)


def upstream_thread(return_value, ip='127.0.0.1'):
    try:
        from time import sleep

        import zmq

        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect(f'tcp://{ip}:48546')
        sleep(0.1)  # wait for binding

        for send_message, recv_message in zip(upstream_send_message, upstream_recv_message):
            socket.send_json(send_message)
            sleep(0.1)
            assert socket.recv_json() == recv_message
            sleep(0.1)
    except Exception as e:
        return_value.append(e)


def ai_thread(capsys, return_value):
    import logging

    from dream.agent.entangled_endive import Agent

    from random import seed

    agent = Agent('TestAgent', 48546, level=logging.DEBUG)
    seed(0)
    agent.run()

    stdout, stderr = capsys.readouterr()
    return_value.extend(stderr.splitlines())


if 'TRAVIS' not in os.environ:  # disable CI tests due to 3rd party dependencies
    def test_ai(capsys):
        from time import sleep
        from threading import Thread

        ai_return_value, upstream_return_value = [], []

        threads = [
            Thread(target=ai_thread, args=(capsys, ai_return_value)),
            Thread(target=upstream_thread, args=(upstream_return_value,)),
        ]

        for i in threads:
            i.daemon = True
            i.start()
            sleep(0.1)
        for i in threads:
            i.join(timeout=20)

        for exception in upstream_return_value:
            raise exception

        assert len(ai_message) == len(ai_return_value)

        for return_value, pattern in zip(ai_return_value, ai_message):
            assert return_value.find(pattern) != -1
