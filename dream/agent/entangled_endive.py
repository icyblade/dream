import gc
import logging
import traceback

import zmq

from . import BaseAgent
from ..bluff import BaseBluff
from ..game.observation import Observation
from ..handcard import BaseHandCard
from ..logger import build_logger
from ..policy.win_rate_based import WinRateBased as Policy
from ..style import BaseStyle
from ..value import BaseValue


class Agent(BaseAgent):
    """Entangled Endive Texas Hold'em AI.

    Parameters
    --------
    name: str
        Name of agent.
    port: int
        Port to be bound.
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

        self.policy = Policy()
        self.value = BaseValue()
        self.style = BaseStyle()
        self.bluff = BaseBluff()
        self.handcard = BaseHandCard()

        self._token = None
        self._request_id = None

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, value):
        # TODO: NOT thread safe
        self._token = value

    @property
    def request_id(self):
        return self._request_id

    @request_id.setter
    def request_id(self, value):
        # TODO: NOT thread safe
        self._request_id = value

    def __del__(self):
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
        str_exception = str(exception)

        if isinstance(exception, SystemExit):
            msg = {'RS': {'errcode': 0, 'errmsg': str_exception}}
            self.logger.info(f'SystemExit captured: {str_exception}.')
            self.logger.debug(f'Sending exception: {msg}.')
        else:
            msg = {'RS': {'errcode': 1, 'errmsg': str_exception}}
            self.logger.error(f'Exception raised: {str_exception}.')
            self.logger.error(traceback.format_exc())
            self.logger.debug(f'Sending exception: {msg}.')
        msg = self._socket.send_json(msg)

        return msg

    def run(self):
        """Run the agent."""
        self.logger.info(f'Agent {self.name} started, binding at tcp://*:{self._port}.')

        while True:
            gc.collect()

            msg = self.observe()
            try:
                self._validate_message(msg)
                self.token = msg['RQ']['token']
                self.request_id = msg['RQ']['requestID']
                msg_type = self._get_message_type(msg)

                if msg_type == 'PLAYERACTION':
                    observation = Observation()
                    observation.update_json(msg['RQ']['data'])
                    action = self.policy.act(observation, None, None)
                    self.logger.debug(f'Acting action: {action}.')
                    self.act(action)
                elif msg_type == 'DELETE':
                    self.send_exception(SystemExit('Agent exits due to DELETE command'))
                    return
                else:
                    self.send_exception(ValueError(f'Unknown message type: {msg_type}'))
            except Exception as e:
                self.send_exception(e)
                continue

    @staticmethod
    def _validate_message(msg):
        """Validate message.

        Parameters
        --------
        msg: obj
            Message object to be validated.

        Raises
        --------
        ValueError
            If `msg` is invalid.
        """
        if 'RQ' not in msg or 'token' not in msg['RQ'] or 'requestID' not in msg['RQ']:
            raise ValueError('Invalid message.')

    @staticmethod
    def _get_message_type(msg):
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
