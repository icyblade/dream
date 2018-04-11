class BaseAgent(object):
    """Abstract class of agent."""

    def __init__(self):
        self.policy = None
        self.value = None
        self.style = None
        self.bluff = None
        self.handcard = None

    @property
    def in_game(self):
        """Is current Agent in game or not."""

        return

    def run(self):
        pass

    def observe(self):
        """Get new observations."""

        pass

    def act(self, action):
        """Do actions."""

        pass
