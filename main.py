import random
import re
from collections import Counter

class FSGState:
    def __init__(self, name: str, is_start: bool = False, is_end: bool = False):
        self.name = name
        self.is_start = is_start
        self.is_end = is_end
        self.inbound = []
        self.outbound = []


class FSGFiniteStateMachine:
    def __init__(self):
        self.start = None
        self.end = None
        self.states = {}

    def add_state(self, state: FSGState):
        self.states[state.name] = state

        if state.is_start:
            self.start = state.name

        if state.is_end:
            self.end = state.name

    def add_transition(self, state_a: str, state_b:  str, transition: str = ""):
        self.states[state_a].outbound.append((state_b, transition))
        self.states[state_b].inbound.append((state_a, transition))

    def generate_test_strings(self, num_samples: int = 100):
        for i in range(num_samples):
            current_state = self.states[self.start]
            trajectory = []
            while not current_state.is_end:
                outbound_choice_index = random.randrange(len(current_state.outbound))
                outbound_transition = current_state.outbound[outbound_choice_index]
                trajectory.append(outbound_transition[1])
                current_state = self.states[outbound_transition[0]]

            yield "".join(trajectory[1:])  # remove initial ^

    def reverse_match(self, test_string: str):
        rev_test_string = f"^{test_string}"[::-1]
        return self._reverse_match(self.states[self.end], rev_test_string)

    def _reverse_match(self, start, rev_test_string):
        current_state = start

        while not current_state.is_start:
            found = []
            for inbound in current_state.inbound:
                if inbound[1] == rev_test_string[:len(inbound[1])]:
                    found.append(inbound)

            if len(found) == 0:
                return False
            elif len(found) > 0:
                any_subtree_match = False
                for state, transition in found:
                    remaining_substring = rev_test_string[len(transition):]
                    if self._reverse_match(self.states[state], remaining_substring):
                        any_subtree_match = True
                return any_subtree_match
        return True


def build_state_machine():
    FSG = FSGFiniteStateMachine()

    FSG.add_state(FSGState("^", is_start=True))
    FSG.add_state(FSGState("qa"))
    FSG.add_state(FSGState("qb"))
    FSG.add_state(FSGState("qc"))
    FSG.add_state(FSGState("qd", is_end=True))

    FSG.add_transition("^", "qa", "^")

    # Qa
    FSG.add_transition("qa", "qb", "f")
    FSG.add_transition("qa", "qd", "s")
    FSG.add_transition("qa", "qc", "g")

    # Qb
    FSG.add_transition("qb", "qd", "gg")
    FSG.add_transition("qb", "qa", "s")

    # Qc
    FSG.add_transition("qc", "qa", "ff")
    FSG.add_transition("qc", "qa", "g")
    FSG.add_transition("qc", "qb", "s")
    FSG.add_transition("qc", "qd", "g")

    return FSG


def run_regex_tests(regex_to_test, samples):
    print("\nRunning regex tests ...\n")
    passed = Counter()
    failed = Counter()

    for string in samples:
        for regex in regex_to_test:
            if re.search(regex, string) is not None:
                passed[regex] += 1
            else:
                failed[regex] += 1

    for regex in regex_to_test:
        print(f"'{regex}' -> passed {passed[regex]} out of {passed[regex] + failed[regex]}")


def test_reverse_match(state_machine: FSGFiniteStateMachine, num_samples: int = 100):
    errors = 0
    for string in state_machine.generate_test_strings(num_samples):
        if not state_machine.reverse_match(string):
            errors += 1

    if errors > 0:
        print("reverse match not implemented correctly!")
        return False
    else:
        print("reverse match implemented correctly!")
        return True


def generate_random_sample_strings(characters: str, num_samples: int = 100):
    chars = characters.split()
    num_possibilities = len(chars)

    for i in range(num_samples):
        random.shuffle(chars)
        string = []
        while random.randrange(num_possibilities + 1) != 0:
            string.append(chars[random.randrange(num_possibilities)])

        yield "".join(string)


def run_reverse_tests(regex_to_test, state_machine: FSGFiniteStateMachine, samples):
    print("\nRunning reverse tests ...\n")

    passed = Counter()
    failed = Counter()

    for sample in samples:
        for regex in regex_to_test:
            test_with_regex = re.search(regex, sample) is not None
            test_with_reverse_match = state_machine.reverse_match(sample)

            if test_with_regex != test_with_reverse_match:
                failed[regex] += 1
            else:
                passed[regex] += 1

    for regex in regex_to_test:
        print(f"'{regex}' -> passed {passed[regex]} out of {passed[regex] + failed[regex]}")


if __name__ == '__main__':
    FSG = build_state_machine()

    # test_reverse_match(FSG, 1000)

    regex_to_test = [
        "^(gff|gss|ff|sf)*(fgg|gsgg|s|gg)$",
        "^((g?(ss|g))|fs)+(s|gsgg|gg)$",
        "^([f|s|g]+(fs|gss|fs))*(fgg|s|gs[gg|s]*)$",
        "^((g(ss|ff|g))|fs)*(s|((f|gs)?gg))$"
    ]

    # run forward tests
    run_regex_tests(regex_to_test, FSG.generate_test_strings(100000))

    # run reverse tests
    run_reverse_tests(regex_to_test, FSG, generate_random_sample_strings("f s g | a", 100000))















