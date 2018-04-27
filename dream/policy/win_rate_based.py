try:
    from pokerai.utils.card_utils import estimate_heads_up_win_rate
    from pokerai.utils.action_utils import inference
    from pokerai.preflop import preflop_inf
except ImportError:
    raise ImportError('Third-party library pokerai created by Guoyong Liu is required for policy WinRateBased.')

import numpy as np

from . import BasePolicy
from ..game.action import Action
from ..game.log_parser import GreatMasterOfPoker
from ..handcard.random_model import RandomModel as HandCard


class WinRateBased(BasePolicy):
    """PokerAI v3.1.

    Policy based on win rate.

    Parameters
    --------
    mapfunc: callable
        A function maps [0, 1] to [0, 1]. Default: $x^2$.
    bluff: callable
        A function maps [0, 1] to [0, 1]. Default: $\sin{x}$.
    decay: callable
        A function maps [0, 1] to [0, 1]. Default: $1-x$.
    weights: list of three int
        Weights of mapfunc, bluff and decay. Default: [1, 1, 1].
    wr_action_curve: callable
        A function maps [0, 1] to [0, 1]. Default: $\frac{9}{8}x^2-\frac{1}{8}$.
    """
    def __init__(self, mapfunc=None, bluff=None, decay=None, weights=None, wr_action_curve=None):
        super(WinRateBased, self).__init__()

        self.mapfunc = lambda x: x ** 2 if mapfunc is None else mapfunc
        self.bluff = np.sin if bluff is None else bluff
        self.decay = lambda x: 1 - x if decay is None else decay
        self.weights = [1, 1, 1] if weights is None else weights
        self.wr_action_curve = lambda x: 9/8*x**2 - 1/8 if wr_action_curve is None else wr_action_curve
        self.handcard = HandCard()

    def act(self, observation, reward, done):
        if observation.board is None:
            # preflop
            game = GreatMasterOfPoker(observation.log)
            action = preflop_inf(game)
            if action.startswith('raise'):
                _, raise_from, _, raise_to = action.split(' ')
                return Action(f'RAISE {raise_to[1:]}', raise_from=raise_from[1:])
            else:
                return Action(action)
        else:
            hole_card = map(str, observation.combo)
            community_card = map(str, observation.board)
            opponents_card_prob_li = (
                (map(str, combo), prob)
                for combo, prob in self.handcard.predict_proba(observation, None)
            )  # TODO: multiple opponents?

            p_strength = estimate_heads_up_win_rate(hole_card, opponents_card_prob_li, community_card=community_card)
            score = inference(p_strength, self.mapfunc, self.bluff, self.decay, weights=self.weights)

            chips = observation.chips
            raise_value = chips * self.wr_action_curve(score)

            if raise_value == 0:
                return Action('CALL')
            else:
                return Action(f'RAISE {raise_value}')
