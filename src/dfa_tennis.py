"""
DFA:
    Deterministic finite automata

state generator
    generate graph from fewer information than the graph itself

define a graph 
    many ways

graph executor
    only compatable with one form of graph

graph analyzer
    - is a graph complete, inescapable, 
    - identify terminal states

graph predictor / optimizer
    - develop shortcuts by hashed chains for knowing if a path is possible
    - programs become compresseds

the set of strings accepted by an automaton is a regular language
valid programs are strings which lead from the start state to a terminal state
 
if the graph is an automaton, lets call A
L(A) is the set of strings accepted by A, or the language of A

there may be no terminal states

final states seem to have to be apriori explicitly defined. 
while terminal states can be discovered, a final state is a given property, not emergent
a state can be final without being terminal. and a terminal state may not be final

are all multi state automata reducible to a single state automata?
are some automata reversible?f
    - is that just a matter of arranging the states such that they contain a history of the previous state?
    - so all history preserving graphs must be a certain size above the non history preserving graph

automata that generate graphs, and can do appending, should be able to count to arbitrary numbers
as long as we do add on only, not remove, we shouldnt invalidate the graph

forward states are not terminal, but are one way. no other states ahead of them can lead back to them.


"""

from typing import Tuple

from common import state_size


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

# state, action_next_state pair
# sans


def find_terminal_states(graph):
    """state where all actions lead to the same state"""
    terminal_states = []
    for state, actions in graph:
        terminal = True
        for _, next_state in actions:
            if next_state != state:
                terminal = False
                break
        if terminal:
            terminal_states.append(state)
    return terminal_states


def find_unreachable_states(graph, starting_states):
    """find states where no actions lead to them"""
    unreachable_states = []

    for state, _ in graph:
        reachable = False
        if state in starting_states:
            reachable = True
            continue

        for _, anap in graph:
            for _, next_action in anap:
                if next_action == state:
                    reachable = True
                    break
            if reachable == True:
                break
        if reachable == False:
            unreachable_states.append(state)

    return unreachable_states


def get_dimensionality(graph):
    num_states = len(graph)
    num_branches = 0
    for state, action_next_state_pairs in graph:
        for action, next_state in action_next_state_pairs:
            if next_state != state:
                num_branches += 1

    return num_branches / num_states


# ts = find_terminal_states(tennis)
# print(ts)


class InvalidAction(Exception):
    pass


class InvalidState(Exception):
    pass


def find(entry, list):
    for item in list:
        if item[0] == entry:
            return item
    return None


def execute_program(
    actions, graph, starting_state, final_states
) -> Tuple[bool, str, int] | Exception:
    current_state = starting_state
    steps = 0

    for action in actions:
        sans = find(current_state, graph)
        if sans is None:
            raise InvalidState(f"State {current_state} is not in the graph")

        state, action_next_state_pairs = sans
        action_next_state = find(action, action_next_state_pairs)
        if action_next_state is None:
            raise InvalidAction(
                f"Action {action} is not valid for state {current_state}"
            )

        action, next_state = action_next_state
        current_state = next_state

        steps += 1

    valid = current_state in final_states
    return valid, current_state, steps


unreachable_states = find_unreachable_states(
    tennis,
    # [],
    ["love"],
)
print(f"Unreachable States: {unreachable_states}")

program = "sosososososs"
valid, current_state, steps = execute_program(program, tennis, tennis_start, ("game",))
print(
    f"Program: {program} is valid: {valid}, current state: {current_state}, steps: {steps}"
)

# print state size
print(f"State size: {state_size(tennis)}")
print(f"Dimensionality: {get_dimensionality(tennis)}")
