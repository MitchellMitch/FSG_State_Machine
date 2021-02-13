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

            yield "".join(trajectory)


    def reverse_match(self, test_string: str):
        rev_test_string = test_string[::-1]

        current_state = self.states[self.end]

        while not current_state.is_start:
            print(current_state)


def build_state_machine():
    FSG = FSGFiniteStateMachine()

    FSG.add_state(FSGState("^", is_start=True))
    FSG.add_state(FSGState("qa"))
    FSG.add_state(FSGState("qb"))
    FSG.add_state(FSGState("qc"))
    FSG.add_state(FSGState("qd", is_end=True))

    FSG.add_transition("^", "qa", "")

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

if __name__ == '__main__':
    FSG = build_state_machine()

    regex_to_test = [
        "^(gff|gss|ff|sf)*(fgg|gsgg|s|gg)$",
        "^((g?(ss|g))|fs)+(s|gsgg|gg)$",
        "^([f|s|g]+(fs|gss|fs))*(fgg|s|gs[gg|s]*)$",
        "^((g(ss|ff|g))|fs)*(s|((f|gs)?gg))$"
    ]

    num_samples = 100000
    run_regex_tests(regex_to_test, FSG.generate_test_strings(num_samples))

        #print(failed)





