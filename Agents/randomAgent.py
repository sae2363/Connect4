from Agents.ASPtwo import StateT, ActionT
from Agents.agent import AdversarialAgent
import point as p
import random


class randomAgent(AdversarialAgent[StateT, ActionT]):
    """A user interface for adversarial search problems as a read-eval-print loop."""

    def choose_action(self, state: StateT) -> ActionT:
        """Select an action for the given state using the agent's strategy.

        A agent that choose moves randomly

        :param      state       Game state
        :returns    Action chosen by the agent
        """
        curr_player_str = self._problem.player(state)
        aList=[]
        for a in self._problem.actions(state):
            aList.append(a)
        action=random.choice(aList)

        #assert action in legal_actions, "User input must convert to a legal action"
        return action

