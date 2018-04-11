from .card import Card


class Observation(object):
    """Observation of Texas Hold'em."""

    def __init__(self):
        self._board = None
        self._combo = None
        self._seat = None
        self._pots = {}
        self._chips = None
        self.raw = {'json': [], 'log': []}

    def update_json(self, json):
        self.raw['json'].append(json)
        self._parse_json()

    def update_log(self, log):
        self.raw['log'].append(log)

    def _parse_json(self):
        combo = list(map(
            lambda x: Card(x),
            self.raw['json'][-1]['playerAction']['player']['card'].split(' ')
        ))
        if self.combo is not None:
            assert self.combo == combo
        else:
            self.combo = combo

        seat = int(self.raw['json'][-1]['playerAction']['player']['position'])
        if self.seat is not None:
            assert self.seat == seat
        else:
            self.seat = seat

        self.pots = self.raw['json'][-1]['playerAction']['pots']
        self.chips = self.raw['json'][-1]['playerAction']['player']['chips']

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

    @property
    def pots(self):
        """Get current pots.

        Returns
        --------
        dict
            Current pots, including side pots.
        """
        return self._pots

    @pots.setter
    def pots(self, value):
        """Set current pots.

        Parameters
        --------
        value: dict
            Current pots. For example: `{'pot': 64}`.
        """
        self._pots = dict([
            (key, float(value_))
            for key, value_ in value.items()
        ])

    @property
    def chips(self):
        """Get chips of current player.

        Returns
        --------
        float
            Chips of current player.
        """
        return self._chips

    @chips.setter
    def chips(self, value):
        """Set chips of current player.

        Parameters
        --------
        value: float
            Chips of current player to be set. For example: `10`.
        """
        self._chips = float(value)

    def to_numeric(self):
        """Convert Observation to numeric values.

        Used for label binarization.
        """
        result = [self.seat]
        for i in self.combo:
            result.append(i.to_numeric())
        return result
