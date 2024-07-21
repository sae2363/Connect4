from ..ASP import StateT, ActionT
import board
from agent import AdversarialAgent
import point as p


class realAgent(AdversarialAgent[StateT, ActionT]):
    """A user interface for adversarial search problems as a read-eval-print loop."""

    def choose_action(self, state: StateT) -> ActionT:
        """Select an action for the given state using the agent's strategy.

        A REPL-based agent prompts the user via commandline to select the next move.

        :param      state       Game state
        :returns    Action chosen by the agent
        """
        curr_player_str = self._problem.player(state)

        # Compute all legal moves and convert them to strings for printing
        legal_actions = self._problem.actions(state)
        move_strings = [point.str() for point in legal_actions]

        assert move_strings, "Cannot prompt user to choose from zero legal moves!"

        user_input = None
        while True:  # Read user's input until a valid move is given
            user_input = input(
                f"Please select a legal move for {curr_player_str} ('q' to quit):"
                + f"\n{move_strings}\n"
            ).strip()

            if user_input == "q":  # Quit the program if the user inputs "q"
                exit()

            if user_input in move_strings:
                break
            else:
                print(f'Invalid move "{user_input}" given. Please try again!\n')

        print("Move accepted, making it now...")

        action = p(user_input.strip("(",")")[0],user_input.strip("(",")")[2])

        assert action in legal_actions, "User input must convert to a legal action"
        return action

