class BasePolicy(object):
    """Abstract class of policy function."""

    def act(self, observation, reward, done):
        """Take action according to observations.

        Parameters
        --------
        observation: instance of dream.game.observation.Observation.
        reward: instance of dream.game.reward.Reward.
        done: bool.

        Returns
        --------
        action: instance of dream.game.action.Action.
        """

        pass
