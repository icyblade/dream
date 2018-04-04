from . import BaseHandCard
from ..game.card import Rank, Suit, Card
from itertools import product
from random import random


class RandomModel(BaseHandCard):
    """Calculate hand card distribution randomly."""

    def predict_proba(self, observation, opponent_name):
        result = []
        for rank_1, suit_1, rank_2, suit_2 in product(Rank.__members__.values(), Suit.__members__.values(),
                                                      Rank.__members__.values(), Suit.__members__.values()):
            combo = [Card(f'{Rank(rank_1)}{Suit(suit_1)}'), Card(f'{Rank(rank_2)}{Suit(suit_2)}')]
            if combo[0].to_numeric() > combo[1].to_numeric():
                result.append((combo, random()))

        sum_weights = sum(([value for key, value in result]))
        result = [
            (key, value/sum_weights)
            for key, value in result
        ]

        return result
