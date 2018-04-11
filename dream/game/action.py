from aenum import MultiValueEnum


class BaseAction(MultiValueEnum):
    ALLIN = 'ALLIN', -3
    CALL = 'CALL', -2
    CHECK = 'CHECK', -1
    FOLD = 'FOLD', 0
    RAISE = 'RAISE'

    def __repr__(self):
        """repr.

        For example: BaseAction(ALLIN).
        """
        return f'BaseAction({self.value})'

    def __str__(self):
        """str.

        For example: ALLIN.
        """
        return str(self.value)


BASE_ACTION_RAISE = BaseAction('RAISE')


class Action(object):
    """Action of Texas Hold'em.

    Parameters
    --------
    action: str
        Raw action string. One of FOLD, CALL, CHECK, ALLIN, RAISE <quantity>.
        For example: RAISE 100 means the player raises to $100.
    raise_from: float
        Optional, specify raise_from value if action is RAISE.
    """
    def __init__(self, action, raise_from=None):
        self._action = None
        self._value = None  # raise to
        self._base_value = None  # raise from

        if isinstance(action, str):
            self._parse_action_from_string(action)
        elif isinstance(action, BaseAction) and action != BASE_ACTION_RAISE:
            self._parse_action_from_base_action(action)
        else:
            raise ValueError(f'Invalid action found: {action}.')

        if raise_from is not None:
            self.raise_from = float(raise_from)

    def _parse_action_from_string(self, action_string):
        action_type = action_string.strip().upper()
        if action_type.startswith('RAISE'):
            self._action = BASE_ACTION_RAISE
            self._value = float(action_type[len('RAISE'):].strip())  # compatible with raise100 and raise 100
        else:
            self._action = BaseAction(action_type)

    def _parse_action_from_base_action(self, base_action):
        self._action = base_action

    def __repr__(self):
        if self._action == BASE_ACTION_RAISE:
            if self.raise_from is None:
                return f'RAISE {self.raise_to}'
            else:
                return f'RAISE {self.raise_to} from {self.raise_from}'
        else:
            return str(self._action)

    def __eq__(self, other):
        return self._action == other._action and self.raise_from == other.raise_from and self.raise_to == other.raise_to

    @property
    def raise_to(self):
        if self._action == BASE_ACTION_RAISE:
            return self._value
        else:
            return None

    @property
    def raise_from(self):
        if self._action == BASE_ACTION_RAISE:
            return self._base_value
        else:
            return None

    @raise_from.setter
    def raise_from(self, value):
        if self._action == BASE_ACTION_RAISE:
            self._base_value = value
        else:
            raise Exception(f'Base action type should be RAISE, {self._action} found.')

    @property
    def raise_mult(self):
        """Multiplication of this RAISE.

        Generally equals to raise_to / raise_from.

        Returns
        --------
        float
            None will be returned if the action is not RAISE.
        """
        if self.raise_from is not None and self.raise_to is not None:
            return self.raise_to / self.raise_from
