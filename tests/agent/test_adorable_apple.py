ai_true_message = [
    'Agent test started, binding at tcp://127\.0\.0\.1\:10000 & tcp://127\.0\.0\.1\:10001',
    'Receiving message: START',
    'New game dream.agent.adorable_apple/test/[0-9]+ initialized.',
    'Receiving message: START',
    'Already initialized game dream.agent.adorable_apple/test/[0-9]+! Cannot initialize new game.',
    'Receiving message: YOUR TURN.',
    'Receiving message: YOUR TURN.',
    'Receiving message: YOUR TURN.',
    'Receiving message: EXPLOIT.',
    'Unknown message: EXPLOIT.',
    'Receiving message: QUIT.',
    'Agent test terminated.',
]
middleware_recv_true_message = [
    'call', 'call', 'call', 'QUIT'
]


def middleware_send():
    from time import sleep

    import zmq

    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind('tcp://127.0.0.1:10000')
    sleep(0.5)  # wait for binding

    socket.send_string('START')
    sleep(0.1)
    socket.send_string('START')
    sleep(0.1)
    socket.send_string('YOUR TURN')
    sleep(0.1)
    socket.send_string('YOUR TURN')
    sleep(0.1)
    socket.send_string('YOUR TURN')
    sleep(0.1)
    socket.send_string('EXPLOIT')
    sleep(0.1)
    socket.send_string('QUIT')


def middleware_recv(return_value):
    import zmq

    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.setsockopt_string(zmq.SUBSCRIBE, '')
    socket.connect('tcp://127.0.0.1:10001')

    while True:
        msg = socket.recv_string()
        return_value.append(msg)

        if msg == 'QUIT':
            return


def ai(capsys, return_value):
    import logging

    from dream.agent.adorable_apple import Agent

    agent = Agent('test', 'tcp://127.0.0.1:10000', 'tcp://127.0.0.1:10001', level=logging.DEBUG)
    agent.run()

    out, err = capsys.readouterr()
    return_value.append(err)


def test_adorable_apple(capsys):
    import re
    from time import sleep
    from threading import Thread

    ai_return_value = []
    middleware_recv_return_value = []

    threads = [
        Thread(target=ai, args=(capsys, ai_return_value)),
        Thread(target=middleware_recv, args=(middleware_recv_return_value, )),
        Thread(target=middleware_send),
    ]

    for i in threads:
        i.start()
        sleep(0.1)
    for i in threads:
        i.join()

    for index, regex in enumerate(ai_true_message):
        assert re.findall(regex, ai_return_value[0].splitlines()[index])

    assert middleware_recv_return_value == middleware_recv_true_message
