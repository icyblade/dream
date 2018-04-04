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
    action: str.
        Raw action string. One of FOLD, CALL, CHECK, ALLIN, RAISE <quantity>.
        For example: RAISE 100 means the player raises to $100.
    """
    def __init__(self, action):
        self._action = None
        self._value = None

        if isinstance(action, str):
            self._parse_action_from_string(action)
        elif isinstance(action, BaseAction) and action != BASE_ACTION_RAISE:
            self._parse_action_from_base_action(action)
        else:
            raise ValueError(f'Invalid action found: {action}.')

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
            return f'RAISE {self._value}'
        else:
            return str(self._action)

    def get_raise_value(self):
        if self._action == BASE_ACTION_RAISE:
            return self._value
        else:
            return None

    def __eq__(self, other):
        return self._action == other._action and self._value == other._value
