from Agents.ASPtwo import StateT, ActionT,ASP
from abc import ABC
from typing import Generic
from Agents.agent import AdversarialAgent
import Agents.nodeClass as n
import numpy as np


class AlphaBeta(AdversarialAgent[StateT, ActionT], ABC):
    """A game-playing agent that chooses optimal actions using alpha-beta search."""

    def choose_action(self, state: StateT) -> ActionT:
        """Select an action for the given state using the agent's strategy.

        The AlphaBetaAgent chooses actions using full-depth alpha-beta search.
            See AlphaBetaAgent.alpha_beta_search() for the full implementation.

        :param      state       Game state
        :returns    Action chosen by the agent
        """
        player=self._problem.player(state)

        return self.alpha_beta_search(state, player)

    def alpha_beta_search(self, state: StateT, player) -> ActionT:
        """Compute the optimal action for the given state using alpha-beta search.

        Alpha - Value of the best choice yet found for MAX (i.e., highest value)
        Beta - Value of the best choice yet found for MIN (i.e., lowest value)

        Reference: Fig. 5.7 (pg. 170) of Artificial Intelligence: A Modern Approach
            (3rd Edition) by Stuart Russell and Peter Norvig.

        :param      state           Game state
        :returns    Best action for the current player assuming optimal play
        """
        assert not self._problem.is_terminal(
            state
        ), "Alpha-beta search expects a non-terminal state as input"

        best_action = None  # To-be-found optimal action from the given state

        if player == 1: # if turn is MAX
            best_value = -10000
            for action in self._problem.actions(state): # iterate through actions
                # print('MAX action', action) # for debugging
                value = self.min_value(self._problem.result(state, action), -10000, 10000)
                if best_value<value: # get the best score in all the actions
                    best_value = value
                    best_action = action
        else:                                       # if turn is MIN
            best_value = 10000
            for action in self._problem.actions(state):
                value = self.max_value(self._problem.result(state, action), -10000, 10000)
                # print('MIN action', action) # for debugging
                if best_value>value:
                    best_value = value
                    best_action = action

        assert best_action is not None, "We should have found a non-None best action"
        return best_action

    def max_value(self, state: StateT, alpha: float, beta: float) -> float:
        """Find the value of the given state, assuming it's the MAX player's turn.

        :param      state       Game state
        :param      alpha       Value of the best found action for MAX (high value)
        :param      beta        Value of the best found action for MIN (low value)
        :returns    Utility of the game state in which MAX has the next move
        """
        assert self._problem.player(state) == 1, "Expected MAX player!"

        value = 0
        if self._problem.is_terminal(state):
            return self._problem.utility(state)
        value = -10000
        for action in self._problem.actions(state):
            value = max(value, self.min_value(self._problem.result(state, action), alpha, beta))
            if value >= beta:
                return value
            alpha = max(alpha, value)
        return value

    def min_value(self, state: StateT, alpha: float, beta: float) -> float:
        """Find the value of the given state, assuming it's the MIN player's turn.

        :param      state       Game state
        :param      alpha       Value of the best found action for MAX (high value)
        :param      beta        Value of the best found action for MIN (low value)
        :returns    Utility of the game state in which MIN has the next move
        """
        assert self._problem.player(state) == 2, "Expected MIN player!"

        value = 0

        if self._problem.is_terminal(state):
            return self._problem.utility(state)
        value = 10000
        for action in self._problem.actions(state):
            value = min(value, self.max_value(self._problem.result(state, action), alpha, beta))
            if value <= alpha:
                return value
            beta = max(beta, value)
        return value




