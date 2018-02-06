import logging

import zmq

from . import BaseAgent
from ..bluff import BaseBluff
from ..game.observation import Observation
from ..handcard import BaseHandCard
from ..logger import build_logger
from ..policy.regression_v1 import Regression
from ..style import BaseStyle
from ..value import BaseValue


class Agent(BaseAgent):
    """Creamy Coconut Texas Hold'em AI.

    Parameters
    --------
    name: str
        Name of agent.
    port: int
        Port to be binded.
    level: int
        Logging level. Default: logging.WARNING.
    """
    ev_range = 0.0

    def __init__(self, name, port, level=logging.WARNING):
        super(Agent, self).__init__()

        self.name = name
        self.logger = build_logger(f'{__name__}/{self.name}', level=level)

        self._context = zmq.Context()
        self._port = port
        self._socket = self._context.socket(zmq.REP)
        self._socket.bind(f'tcp://*:{port}')

        self.policy = Regression()
        self.value = BaseValue()
        self.style = BaseStyle()
        self.bluff = BaseBluff()
        self.handcard = BaseHandCard()

        self.token = None
        self.request_id = None

    def __del__(self):
        self._socket.close()
        self._socket.close()
        self._context.destroy()

    def observe(self):
        """Get observation.

        Returns
        --------
        obj
            Incoming JSON message, e.g. new observation.
        """
        msg = self._socket.recv_json()
        self.logger.debug(f'Receiving message: {msg}.')
        return msg

    def act(self, action):
        """Do action.

        Parameters
        --------
        action: instance of `dream.game.action.Action`
            Action to be done.

        Returns
        --------
        obj
            Incoming JSON message returned by `action`.
        """
        msg = {
            'RS': {
                'token': self.token,
                'requestID': self.request_id,
                'data': {
                    'playerAction': {
                        'action': repr(action)
                    }
                }
            }
        }
        self.logger.debug(f'Sending message: {msg}.')
        msg = self._socket.send_json(msg)
        return msg

    def send_exception(self, exception):
        """Send exception raised by AI.

        Parameters
        --------
        exception: Exception
            Raised exception.

        Returns
        --------
        obj
            Incoming JSON message returned by `exception`.
        """
        msg = {'RS': {'errcode': 1}}
        self.logger.debug(f'Sending exception: {msg}.')
        msg = self._socket.send_json(msg)
        return msg

    def run(self):
        """Run the agent."""
        self.logger.info(f'Agent {self.name} started, binding at tcp://*:{self._port}.')

        while True:
            msg = self.observe()
            try:
                self._validate_message(msg)
            except Exception as e:
                self.send_exception(e)
                continue

            self.token = msg['RQ']['token']
            self.request_id = msg['RQ']['requestID']
            msg_type = self._get_message_type(msg)

            if msg_type == 'PLAYERACTION':
                observation = Observation()
                observation.combo = msg['RQ']['data']['playerAction']['player']['card'].split(' ')
                observation.seat = int(msg['RQ']['data']['playerAction']['player']['position'])
                action = self.policy.act(observation, None, None)
                self.logger.debug(f'Acting action: {action}.')
                self.act(action)
            elif msg_type == 'DELETE':
                self.send_exception(SystemExit())
                return
            else:
                self.send_exception(Exception())

    def _validate_message(self, msg):
        """Validate message.

        Parameters
        --------
        msg: obj
            Message object to be validated.

        Raises
        --------
        ValueError
            If `msg` is invalid.
        TypeError
            If `msg` has invalid type. (Maybe missing json decoding?)
        """
        if not isinstance(msg, dict):
            raise TypeError

        if 'RQ' not in msg or 'token' not in msg['RQ'] or 'requestID' not in msg['RQ']:
            raise ValueError

    def _get_message_type(self, msg):
        """Determine incoming JSON message type.

        Parameters
        --------
        msg: obj
            Incoming JSON message.

        Returns
        --------
        str
            Message type. Possible values: PLAYERACTION, DELETE and UNKNOWN.
        """
        try:
            return msg['RQ']['action']
        except KeyError:
            return 'UNKNOWN'
