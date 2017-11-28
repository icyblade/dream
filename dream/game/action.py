class Action(object):
    """Action of Texas Hold'em.

    Parameters
    --------
    action_raw: str.
        Raw action string. One of FOLD, CALL, ALLIN, RAISE<quantity>.
        For example: RAISE100 means the player raises to $100.
    """

    def __init__(self, action_raw: str):
        action_type = action_raw.strip()
        if action_type == 'FOLD':
            self.action = -1.0
        elif action_type == 'CALL':
            self.action = 0.0
        elif action_type.startswith('RAISE'):
            action = action_type[len('RAISE'):].strip()
            action = float(action)  # Exploit: float('RAISE INFINITY') is ALLIN
            assert action > 0
            self.action = action
        elif action_type == 'ALLIN':
            self.action = float('inf')
        else:
            raise ValueError

    def __repr__(self):
        return str(self.action)

    @property
    def action(self):
        """Action code.

        Action code is a float from -1 to inf.
        For example: -1 means fold, 0 means call, 100 means the player raise to $100, inf means all in.
        """

        return self._action

    @action.setter
    def action(self, action):
        self._action = action
