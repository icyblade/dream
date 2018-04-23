import os


upstream_send_message = [
    {
        'RQ': {
            'action': 'PLAYERACTION',
            'data': {
                'playerAction': {
                    'boardCards': '',
                    'log': [
                        'PokerStars Hand #124959928530:  Hold\'em No Limit ($10.00/$20.00 USD) - 2014/11/12 8:26:34 ET',
                        'Table \'Grus II\' 6-max Seat #3 is the button',
                        'Seat 1: zazano ($2391 in chips)',
                        'Seat 2: jinmay ($7997.07 in chips)',
                        'Seat 3: davidtan23 ($2053.60 in chips)',
                        'Seat 4: Rednaxela747 ($1007.45 in chips)',
                        'Seat 5: bmlm ($2308.30 in chips)',
                        'Seat 6: heffalump75 ($2433.40 in chips)',
                        'Rednaxela747: posts small blind $10',
                        'bmlm: posts big blind $20',
                        '*** HOLE CARDS ***',
                        'Dealt to bmlm [Kh 4h]',
                        'heffalump75: folds',
                        'zazano: folds',
                        'jinmay: folds',
                        'davidtan23: folds',
                        'davidtan23 said, "unittest: test for colon bypass"',
                        'Rednaxela747: raises $40.80 to $60.80',
                        'bmlm: calls $40.80',
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
                    'action': 'FOLD'
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
        "'data': {'playerAction': {'action': 'FOLD'}}}}"
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


def ai_thread(caplog, return_value):
    import logging

    from dream.agent.entangled_endive import Agent

    from random import seed

    agent = Agent('TestAgent', 48546, level=logging.DEBUG)
    seed(0)
    agent.run()

    return_value.extend([rec.message for rec in caplog.records])


if 'TRAVIS' not in os.environ:  # disable CI tests due to 3rd party dependencies
    def test_ai(caplog):
        from time import sleep
        from threading import Thread

        ai_return_value, upstream_return_value = [], []

        threads = [
            Thread(target=ai_thread, args=(caplog, ai_return_value)),
            Thread(target=upstream_thread, args=(upstream_return_value,)),
        ]

        for i in threads:
            i.daemon = True
            i.start()
            sleep(0.1)
        for i in threads:
            i.join(timeout=5)

        for exception in upstream_return_value:
            raise exception

        assert len(ai_message) == len(ai_return_value)

        for return_value, pattern in zip(ai_return_value, ai_message):
            assert return_value.find(pattern) != -1
