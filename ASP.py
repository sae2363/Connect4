from abc import ABC, abstractmethod
from typing import TypeVar, Generic
from enum import Enum

StateT = TypeVar("StateT")  # Generic type representing a game state
ActionT = TypeVar("ActionT")  # Generic type representing a game move

Player = Enum("Player", ["MAX", "MIN"])

class ASP(Generic[StateT, ActionT], ABC):
    """An adversarial search problem (ASP) representing a two-player, zero-sum game."""

    @abstractmethod
    def initial_state(self) -> StateT:
        """Generate the state representing the game's starting setup.

        :returns    Initial state of the game
        """
        pass

    @abstractmethod
    def player(self, state: StateT) -> Player:
        """Find which player has the move in the given state.

        :param      state       A state of the game
        :returns    Player whose turn it is to move
        """
        pass

    @abstractmethod
    def actions(self, state: StateT) -> set[ActionT]:
        """Compute all legal moves from the given state.

        :param      state       Game state from which actions are identified
        :returns    Set of legal moves in the state
        """
        pass

    @abstractmethod
    def result(self, state: StateT, action: ActionT) -> StateT:
        """Simulate the result of applying the given action in the given state.

        :param      state       Game state in which the action is applied
        :param      action      Action applied in the game
        :returns    Resulting state after applying the action
        """
        pass

    def result_actions(self, state: StateT, actions: list[ActionT]) -> StateT:
        """Simulate the result of applying multiple actions from the given state.

        :param      state       Game state from which the actions are applied
        :param      actions     List of actions
        :returns    Resulting state after applying the actions, in list order
        """
        curr_state = state
        for a in actions:
            curr_state = self.result(curr_state, a)
        return curr_state

    @abstractmethod
    def is_terminal(self, state: StateT) -> bool:
        """Check whether the game is over in the given state.

        :param      state       Game state
        :returns    Boolean indicating if the state is terminal (True = 'Game Over')
        """
        pass

    @abstractmethod
    def utility(self, state: StateT) -> float:
        """Compute the absolute value of the given terminal state.

        This utility is "absolute" in the sense that it corresponds to both players'
            perspectives. For example, MAX always wants 1, MIN always wants 0.

        :param      state       Terminal game state
        :returns    Numeric utility of the state
        """
        pass