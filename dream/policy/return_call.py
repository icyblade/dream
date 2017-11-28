from . import BasePolicy
from ..game.action import Action


class ReturnCall(BasePolicy):
    def act(self, observation, reward, done):
        return Action('CALL')
