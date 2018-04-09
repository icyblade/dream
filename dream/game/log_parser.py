import re
from datetime import datetime

from .player import Player


class Parser(object):

    def __init__(self, log):
        self.log = log

        self.log_id = None
        self.small_blind = None
        self.big_blind = None
        self.currency = None
        self.time = None
        self.table_name = None
        self.max_players = None
        self.button = None
        self.players = []
        self.game_rounds = {}

        self._parse()

    def _parse(self):
        pass

    def get_player(self, seat_id=None, player_name=None):
        """Return the first player found by seat or name.

        Parameters
        --------
        seat_id: int
            Seat of player to be found, starting at 1.
        player_name: str
            Name of player to be found.

        Returns
        --------
        dream.game.player.Player or None
            If player is not found, None will be returned.
            Otherwise the dream.game.player.Player object will be returned.
        """
        if seat_id is None and player_name is None:
            raise ValueError('Either seat_id or player_name should be specified.')

        for player in self.players:
            if (seat_id is None or (seat_id is not None and player.seat_id == seat_id)) and \
                    (player_name is None or (player_name is not None and player.player_name == player_name)):
                return player

        return None


class PokerStars(Parser):
    _header_regex = re.compile(r"""
        PokerStars\s*(Zoom)?\s*Hand\s*
        \#(?P<log_id>[0-9]+)
        \:\s*
        Hold'em\s*No\s*Limit\s*
        \(\S(?P<small_blind>[0-9]+)/\S(?P<big_blind>[0-9]+)\s*(?P<currency>\S+)\)
        \s*\-\s*(?P<time>[0-9/: ]+?)\s*ET
    """, re.X)
    _table_regex = re.compile(r"""
        Table\s*'(?P<table_name>[\s\S]+?)'\s*(?P<max_players>[0-9]+)\-max\s*Seat\s*\#(?P<button>[0-9]+)\s*is\s*the\s*button
    """, re.X)
    _seat_regex = re.compile(r"Seat (?P<seat_id>[0-9]+)\: (?P<player_name>\S+) \(\S(?P<chips>[0-9.]+) in chips\)")
    _game_rounds_regex = re.compile(r"\*\*\* (?P<round_name>[\s\S]+?) \*\*\*")

    _log_attributes = {
        'log_id': int,
        'small_blind': float,
        'big_blind': float,
        'currency': str,
        'time': lambda x: datetime.strptime(x, '%Y/%m/%d %H:%M:%S'),
        'table_name': str,
        'max_players': int,
        'button': int,
        'seat_id': int,
        'chips': float,
    }

    def __init__(self, log):
        super(PokerStars, self).__init__(log=log)

    def _parse(self):
        super(PokerStars, self)._parse()

        # parse header
        regex_results = self._header_regex.search(self.log)
        for value, cast_function in self._log_attributes.items():
            try:
                setattr(self, value, cast_function(regex_results.group(value)))
            except IndexError:
                pass

        # parse table
                regex_results = self._table_regex.search(self.log)
        for value, cast_function in self._log_attributes.items():
            try:
                setattr(self, value, cast_function(regex_results.group(value)))
            except IndexError:
                pass

        # parse players
        regex_results = self._seat_regex.findall(self.log)
        for seat_id, player_name, chips in regex_results:
            self.players.append(Player(
                player_name=player_name,
                seat_id=self._log_attributes['seat_id'](seat_id),
                chips=self._log_attributes['chips'](chips),
            ))

        # split sections
        for text in self._game_rounds_regex.split(self.log):
            pass
