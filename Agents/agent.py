from ..ASP import StateT, ActionT, ASP
from abc import ABC, abstractmethod
from typing import Generic

class AdversarialAgent(Generic[StateT, ActionT], ABC):
    """A game-playing agent defining a strategy for adversarial search problems."""
    _problem: ASP[StateT, ActionT]
    def __init__(self, problem: ASP[StateT, ActionT]):
        """Initialize the agent for a particular adversarial search problem.

        :param      problem     Adversarial search problem
        """
        self._problem = problem

    def agent_string(self) -> str:
        """Return a string describing the type of this agent.

        :returns    String describing the agent's type (e.g., RandomAgent)
        """
        return type(self).__name__

    @abstractmethod
    def choose_action(self, state: StateT) -> ActionT:
        """Select an action for the given state using the agent's strategy.

        :param      state       Game state
        :returns    Action chosen by the agent
        """
        pass