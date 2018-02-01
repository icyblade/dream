class Action(object):
    """Action of Texas Hold'em.

    Parameters
    --------
    action_raw: str.
        Raw action string. One of fold, call, check, allin, raise <quantity>.
        For example: RAISE 100 means the player raises to $100.
    """
    ACTION_MAPPER = {
        'allin': -3.0, 'call': -2.0, 'check': -1.0, 'fold': 0.0,
    }

    def __init__(self, action_raw: str):
        action_type = action_raw.strip().lower()
        if action_type in self.ACTION_MAPPER:
            self.action = self.ACTION_MAPPER[action_type]
        elif action_type.startswith('raise'):
            action = float(action_type[len('raise'):].strip())  # compatible with raise100 and raise 100
            assert action > 0, f'Should always raise a positive quantity. Found: {action}'
            self.action = action
        else:
            raise ValueError('Invalid action: {action_raw}.')

    def __repr__(self):
        if self.action > 0:
            return f'raise {self.action}'

        for k, v in self.ACTION_MAPPER.items():
            if self.action == v:
                return k

        raise ValueError('Invalid instance of Action: {self.action}.')

    @property
    def action(self):
        """Action code.

        Action code is a float from -1 to inf.
        -3 means all-in, -2 means call, -1 means check, 0 means fold, 100 means the player raises to $100.
        """
        return self._action

    @action.setter
    def action(self, action):
        self._action = action
