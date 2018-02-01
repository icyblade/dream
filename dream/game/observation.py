from .card import Card


class Observation(object):
    """Observation of Texas Hold'em

    Parameters
    --------
    observation: str
        Observation string.
    """

    def __init__(self, observation):
        self._board = None
        self._combo = None
        self._seat = None

    @property
    def seat(self):
        """Get seat of current player.

        Returns
        --------
        int
            Seat of current player, starting from 0.
        """
        return self._seat

    @seat.setter
    def seat(self, value):
        """Set seat of current player.

        Parameters
        --------
        value: int
            Seat of current player, starting from 0.
        """
        self._seat = value

    @property
    def combo(self):
        """Get two hand cards of current player..

        Returns
        --------
        list of instance of dream.game.card.Card
            List of two board cards. For example: `['5c', '4s']`.
        """
        return self._combo

    @combo.setter
    def combo(self, value):
        """Set two hand cards of current player..

        Parameters
        --------
        value: list of str
            List of two board cards. For example: `['5c', '4s']`.
        """
        assert isinstance(value, list) or isinstance(value, tuple)
        assert len(value) == 2
        self._combo = list(map(lambda x: Card(x), value))

    @property
    def board(self):
        """Get three board cards.

        Returns
        --------
        list of instance of dream.game.card.Card
            List of three board cards. For example: `['5c', '4s', 'As']`.
        """
        return self._board

    @board.setter
    def board(self, value):
        """Set three board cards.

        Parameters
        --------
        value: list of str
            List of three board cards. For example: `['5c', '4s', 'As']`.
        """
        assert isinstance(value, list) or isinstance(value, tuple)
        assert len(value) == 3
        self._board = list(map(lambda x: Card(x), value))
