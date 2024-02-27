"""
NFA:
    Nondeterministic finite automata
"""

from pprint import pprint
from typing import Tuple

from common import InvalidAction, InvalidState, find

"""
dfa:
tennis_start = "love"
tennis = (
    ("love", (("s", "15-love"), ("o", "love-15"))),
    ("15-love", (("s", "30-love"), ("o", "15-all"))),
    ("love-15", (("s", "15-all"), ("o", "love-30"))),
    ("15-all", (("s", "30-15"), ("o", "15-30"))),
    ("30-love", (("s", "40-love"), ("o", "30-all"))),
    ("love-30", (("s", "15-40"), ("o", "love-40"))),
    ("30-15", (("s", "40-15"), ("o", "30-all"))),
    ("15-30", (("s", "15-40"), ("o", "15-40"))),
    ("30-all", (("s", "40-30"), ("o", "30-40"))),
    ("40-love", (("s", "game"), ("o", "40-15"))),
    ("love-40", (("s", "15-40"), ("o", "game"))),
    ("40-15", (("s", "game"), ("o", "40-30"))),
    ("15-40", (("s", "15-40"), ("o", "game"))),
    ("40-30", (("s", "game"), ("o", "deuce"))),
    ("30-40", (("s", "deuce"), ("o", "game"))),
    ("deuce", (("s", "ad-in"), ("o", "ad-out"))),
    ("ad-out", (("s", "deuce"), ("o", "game"))),
    ("ad-in", (("s", "game"), ("o", "deuce"))),
    ("game", (("s", "game"), ("o", "game"))),
)

"""

# for reference
# board = (
#     (1, 2, 3),
#     (4, 5, 6),
#     (7, 8, 9),
# )

# NFA
chess = (
    (1, (("r", (2, 4)), ("b", (5,)))),
    (2, (("r", (4, 6)), ("b", (1, 3, 5)))),
    (3, (("r", (2, 6)), ("b", (5,)))),
    (4, (("r", (2, 8)), ("b", (1, 5, 7)))),
    (5, (("r", (2, 4, 6, 8)), ("b", (1, 3, 7, 9)))),
    (6, (("r", (2, 8)), ("b", (3, 5, 9)))),
    (7, (("r", (4, 8)), ("b", (5,)))),
    (8, (("r", (4, 6)), ("b", (5, 7, 9)))),
    (9, (("r", (6, 8)), ("b", (5,)))),
)
chess_final_states = (9,)

program = "rbb"


def execute_program(actions, graph, starting_state, final_states):
    current_states = [starting_state]
    steps = 0

    for action in actions:
        new_states = []
        for current_state in current_states:
            sans = find(current_state, graph)
            if sans is None:
                raise InvalidState(f"State {current_state} is not in the graph")

            _, action_next_states_pairs = sans
            action_next_states = find(action, action_next_states_pairs)
            if action_next_states is None:
                raise InvalidAction(
                    f"Action {action} is not valid for state {current_state}"
                )

            _, next_states = action_next_states
            for state in next_states:
                if state not in new_states:
                    new_states.append(state)

        current_states = new_states

        steps += 1
        print(f"{steps}: {current_states}")

    valid = any(state in final_states for state in current_states)
    return valid, current_states, steps


def convert_nfa_to_dfa(nfa, initial_state, final_states):
    pass


valid, current_states, steps = execute_program(program, chess, 1, (9,))
print(f"Valid: {valid}, Current States: {current_states}, Steps: {steps}")
