from ..ASP import StateT, ActionT,ASP
from abc import ABC
from typing import Generic
from agent import AdversarialAgent

class MCTS(AdversarialAgent[StateT, ActionT], ABC):
    """A game-playing agent defining a strategy for adversarial search problems."""

    def choose_action(self, state: StateT) -> ActionT:
        """Select an action for the given state using the agent's strategy.

        :param      state       Game state
        :returns    Action chosen by the agent
        """
        return self.MCTS(state)
    def MCTS(self,state:StateT)-> ActionT:
        assert not self._problem.is_terminal(
            state
        ), "Alpha-beta search expects a non-terminal state as input"
        #program the algorithm 
        """
        idea so far

        while loop
        make a tree with nodes to store the data up to n deep
        go to a leaf of the tree and start randomly pick moves till terminal state is reached
        with this result, go up child node till hit root and update
        pick the actions with the highest win rate
        question right now do i save the tree to use later or not
        """