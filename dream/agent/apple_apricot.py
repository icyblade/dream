import logging
from time import time

import zmq

from . import BaseAgent
from ..bluff import BaseBluff
from ..handcard import BaseHandCard
from ..logger import build_logger
from ..policy.return_call import ReturnCall
from ..style import BaseStyle
from ..value import BaseValue


class Agent(BaseAgent):
    def __init__(self, name, recv_addr, send_addr, level=logging.WARNING):
        super(Agent, self).__init__()

        self.name = name
        self.logger = build_logger(f'{__name__}/{self.name}', level=level)

        self._context = zmq.Context()
        self._recv_addr = recv_addr
        self._recv_socket = self._context.socket(zmq.SUB)
        self._recv_socket.setsockopt_string(zmq.SUBSCRIBE, '')  # subscribe everything
        self._recv_socket.connect(self._recv_addr)
        self._send_addr = send_addr
        self._send_socket = self._context.socket(zmq.PUB)
        self._send_socket.bind(self._send_addr)

        self.game_id = None

        self.policy = ReturnCall()
        self.value = BaseValue()
        self.style = BaseStyle()
        self.bluff = BaseBluff()
        self.handcard = BaseHandCard()

    @property
    def in_game(self):
        return self.game_id is not None

    def observe(self):
        return self._recv_socket.recv_string()

    def act(self, action):
        return self._send_socket.send_string(action)

    def run(self):
        self.logger.info(f'Agent {self.name} started, binding at {self._recv_addr} & {self._send_addr}.')
        while True:
            msg = self.observe()
            self.logger.debug(f'Receiving message: {msg}.')
            msg_type = self._get_message_type(msg)

            if msg_type == 'START':
                if not self.in_game:
                    self.game_id = f'{__name__}/{self.name}/{int(time())}'
                    self.logger.info(f'New game {self.game_id} initialized.')
                else:
                    self.logger.critical(f'Already initialized game {self.game_id}! Cannot initialize new game.')
                action = self.policy.act(msg, None, False)
                self.act(action)
            elif msg_type == 'YOUR TURN' and self.in_game:
                action = self.policy.act(msg, None, False)
                self.act(action)
            elif msg_type == 'QUIT' and self.in_game:
                self.game_id = None
                action = self.policy.act(msg, None, True)
                self.act(action)
                break
            else:
                self.logger.critical(f'Unknown message: {msg}.')

        self.logger.info(f'Agent {self.name} terminated.')

    def _get_message_type(self, msg):
        if msg == 'START':
            return 'START'
        if msg == 'YOUR TURN':
            return 'YOUR TURN'
        if msg == 'QUIT':
            return 'QUIT'
