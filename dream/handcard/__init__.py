import numpy as np


class BaseHandCard(object):
    """Abstract class of handcard function."""

    def predict(self, observation, opponent_name):
        """Predict the most probable hand card of opponent.

        Parameters
        --------
        observation: instance of dream.game.observation.Observation
        opponent_name: str
            Name of opponent to be guessed.

        Returns
        --------
        list of dream.game.card.Card
            Two cards the opponent takes.
        """
        distribution = self.predict_proba(observation, opponent_name)

        return max(distribution, key=lambda x: x[1])[0]

    def predict_proba(self, observation, opponent_name):
        """Calculate the hand card distribution of opponent.

        Parameters
        --------
        observation: instance of dream.game.observation.Observation
        opponent_name: str
            Name of opponent to be guessed.

        Returns
        --------
        list
            Hand card distribution, list(([dream.game.card.Card, dream.game.card.Card], float)).
        """
        pass
