import re
from datetime import datetime

from .action import Action
from .card import Card
from .player import Player


class Parser(object):
    _valid_game_rounds = {}

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
        self._game_rounds = {}
        self.current_handcard = None
        self.actions = dict([(round, []) for round in self._valid_game_rounds])
        self.community_cards = []

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
        dream.game.player.Player
            The player found will be returned as dream.game.player.Player.

        Raises
        --------
        ValueError
            A ValueError will be raised if no player is found.
        """
        if seat_id is None and player_name is None:
            raise ValueError('Either seat_id or player_name should be specified.')

        for player in self.players:
            if (seat_id is None or (seat_id is not None and player.seat_id == seat_id)) and \
                    (player_name is None or (player_name is not None and player.player_name == player_name)):
                return player

        raise ValueError(f'Invalid player.')

    def get_actions(self, game_round):
        if game_round not in self._valid_game_rounds:
            raise ValueError(f'Invalid game round name: {game_round}')

        try:
            return self.actions[game_round]
        except KeyError:
            return None


class PokerStars(Parser):
    _header_regex = re.compile(r"""
        PokerStars\s*(Zoom)?\s*Hand\s*
        \#(?P<log_id>\d+)
        \:\s*
        Hold'em\s*No\s*Limit\s*
        \(\S(?P<small_blind>\d+)/\S(?P<big_blind>\d+)\s*(?P<currency>\S+)\)
        \s*\-\s*(?P<time>[\d/: ]+?)\s*ET
    """, re.X)
    _table_regex = re.compile(r"""
        Table\s*'(?P<table_name>.+?)'\s*(?P<max_players>\d+)\-max\s*Seat\s*\#(?P<button>\d+)\s*is\s*the\s*button
    """, re.X)
    _seat_regex = re.compile(r"Seat (?P<seat_id>\d+)\: (?P<player_name>\S+) \(\S(?P<chips>[\d.]+) in chips\)")
    _game_rounds_regex = re.compile(r"\*\*\* (?P<round_name>.+?) \*\*\*")

    _action_regex = re.compile(r"(?P<player_name>.+?)\: (?P<action>.+)")
    _raise_regex = re.compile(r"raises .(?P<raise_from>[\d.]+) to .(?P<raise_to>[\d.]+)")
    _bet_regex = re.compile(r"bets .(?P<raise_to>[\d.]+)")
    _allin_regex = re.compile(r".*? and is all-in")

    _handcard_regex = re.compile(r"Dealt to (?P<player_name>.+?) \[(?P<handcard>.{5})\]")
    _flop_card_regex = re.compile(r"\[(?P<cards>.{8})\]")

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

    _valid_game_rounds = {'preflop', 'flop', 'turn', 'river', 'show down', 'summary'}

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

        # split rounds
        current_round = None
        for text in self._game_rounds_regex.split(self.log):
            if text == 'HOLE CARDS':
                current_round = 'preflop'
            elif text == 'FLOP':
                current_round = 'flop'
            elif text == 'TURN':
                current_round = 'turn'
            elif text == 'RIVER':
                current_round = 'river'
            elif text == 'SHOW DOWN':
                current_round = 'show down'
            elif text == 'SUMMARY':
                current_round = 'summary'
            else:
                if current_round is None:
                    pass
                else:
                    self._game_rounds[current_round] = text

        self._parse_game_round_preflop()
        self._parse_game_round_flop()

    def _parse_game_round_preflop(self):
        log = self._game_rounds['preflop']
        regex_result = self._handcard_regex.search(log)
        player_name = regex_result.group('player_name')
        player = self.get_player(player_name=player_name)

        self.current_player = player
        self.current_handcard = list(map(
            lambda x: Card(x),
            regex_result.group('handcard').split(' ')
        ))

        for player_name, action_string in self._action_regex.findall(log):
            player = self.get_player(player_name=player_name)
            action = self._load_action_from_string(action_string)
            self.actions['preflop'].append((player, action))

    def _parse_game_round_flop(self):
        log = self._game_rounds['flop']
        regex_result = self._flop_card_regex.search(log)
        self.community_cards = list(map(
            lambda x: Card(x),
            regex_result.group('cards').split(' ')
        ))

        for player_name, action_string in self._action_regex.findall(log):
            player = self.get_player(player_name=player_name)
            action = self._load_action_from_string(action_string)
            self.actions['flop'].append((player, action))

    def _load_action_from_string(self, string):
        """Convert raw log string to Action."""
        if self._allin_regex.search(string) is not None:
            return Action('ALLIN')
        elif string.startswith('calls'):
            return Action('CALL')
        elif string == 'checks':
            return Action('CHECK')
        elif string == 'folds':
            return Action('FOLD')
        elif string.startswith('raises'):
            regex_result = self._raise_regex.search(string)
            value = regex_result.group('raise_to')
            return Action(f'RAISE {value}')
        elif string.startswith('bets'):
            regex_result = self._bet_regex.search(string)
            value = regex_result.group('raise_to')
            return Action(f'RAISE {value}')
        else:
            raise ValueError(f'Invalid action from string: {string}.')
