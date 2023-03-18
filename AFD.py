class State:
    def __init__(self):
        self.transitions = {}

class NFA:
    def __init__(self, start_state, end_state):
        self.start_state = start_state
        self.end_state = end_state

    def epsilon_closure(self, state):
        closure = set()
        stack = [state]
        while stack:
            current_state = stack.pop()
            closure.add(current_state)
            for next_state in current_state.transitions.get('', []):
                if next_state not in closure:
                    stack.append(next_state)
        return closure

    def symbols(self):
        symbols = set()
        for state in self.states():
            for symbol in state.transitions.keys():
                if symbol != '':
                    symbols.add(symbol)
        return symbols
    
    def states(self):
        visited = set()
        queue = [self.start_state]
        while queue:
            state = queue.pop(0)
            if state in visited:
                continue
            visited.add(state)
            for symbol, transitions in state.transitions.items():
                for next_state in transitions:
                    queue.append(next_state)
        return visited

    def move(self, states, symbol):
        next_states = set()
        for state in states:
            transitions = state.transitions.get(symbol, [])
            next_states.update(transitions)
        return next_states

def postfix_to_nfa(postfix_expr):
    stack = []

    for c in postfix_expr:
        if c == '*':
            nfa = stack.pop()
            start = State()
            end = State()
            start.transitions[''] = [nfa.start_state, end]
            nfa.end_state.transitions[''] = [nfa.start_state, end]
            stack.append(NFA(start, end))
        elif c == '+':
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            start = State()
            end = State()
            start.transitions[''] = [nfa1.start_state, nfa2.start_state]
            nfa1.end_state.transitions[''] = [end]
            nfa2.end_state.transitions[''] = [end]
            stack.append(NFA(start, end))
        elif c == '.':
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            nfa1.end_state.transitions[''] = [nfa2.start_state]
            stack.append(NFA(nfa1.start_state, nfa2.end_state))
        elif c == '|':
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            start = State()
            end = State()
            start.transitions[''] = [nfa1.start_state, nfa2.start_state]
            nfa1.end_state.transitions[''] = [end]
            nfa2.end_state.transitions[''] = [end]
            stack.append(NFA(start, end))
        else:
            start = State()
            end = State()
            start.transitions[c] = [end]
            stack.append(NFA(start, end))

    return stack.pop()

def print_nfa(nfa):
    print('Initial state:', id(nfa.start_state))
    print('Acceptance state:', id(nfa.end_state))
    print('States:')
    visited = set()
    queue = [nfa.start_state]
    while queue:
        state = queue.pop(0)
        if state in visited:
            continue
        visited.add(state)
        print(id(state), end=' ')
        for symbol, transitions in state.transitions.items():
            for next_state in transitions:
                queue.append(next_state)
    print('\nTransitions:')
    visited = set()
    queue = [(nfa.start_state, '')]
    while queue:
        state, symbol = queue.pop(0)
        if state in visited:
            continue
        visited.add(state)
        for next_state in state.transitions.get(symbol, []):
            queue.append((next_state, symbol))
            print(id(state), '->', id(next_state), symbol)
    print()


class DFAState:
    def __init__(self, nfa_states):
        self.nfa_states = nfa_states
        self.transitions = {}

class DFA:
    def __init__(self, start_state, accept_states):
        self.start_state = start_state
        self.accept_states = accept_states
        self.states = set()
        self.transitions = {}
        self.states.add(start_state)

    def add_state(self, state):
        self.states.add(state)

    def symbols(self):
        symbols = set()
        for state in self.states:
            for symbol in state.transitions.keys():
                if symbol != '':
                    symbols.add(symbol)
        return symbols



def nfa_to_dfa(nfa):
    start_state = DFAState(nfa.epsilon_closure(nfa.start_state))
    dfa_states = [start_state]
    queue = [start_state]
    sigma = nfa.symbols()

    # DFA 
    dfa = DFA(start_state, [])

    while queue:
        dfa_state = queue.pop(0)
        dfa.add_state(dfa_state)

        for symbol in sigma:
            next_nfa_states = nfa.move(dfa_state.nfa_states, symbol)
            if not next_nfa_states:
                continue
            next_dfa_state = None

            for state in dfa_states:
                if next_nfa_states == state.nfa_states:
                    next_dfa_state = state
                    break

            if not next_dfa_state:
                next_dfa_state = DFAState(next_nfa_states)
                dfa_states.append(next_dfa_state)
                queue.append(next_dfa_state)

            dfa_state.transitions[symbol] = next_dfa_state

    return dfa

def print_dfa(dfa):
    print('Initial state:', id(dfa.start_state))
    print('Acceptance states:', [id(state) for state in dfa.accept_states])
    print('States:')
    visited = set()
    queue = [dfa.start_state]
    while queue:
        state = queue.pop(0)
        if state in visited:
            continue
        visited.add(state)
        print(id(state), end=' ')
        for symbol, next_state in state.transitions.items():
            queue.append(next_state)
    print('\nTransitions:')
    visited = set()
    queue = [(dfa.start_state, '')]
    while queue:
        state, symbol = queue.pop(0)
        if state in visited:
            continue
        visited.add(state)
        for symbol, next_state in state.transitions.items():
            queue.append((next_state, symbol))
            print(id(state), '->', id(next_state), symbol)
    print()

from graphviz import Digraph

def graph(dfa):
    dot = Digraph()
    dot.attr(rankdir='LR')
    dot.node(str(id(dfa.start_state)), shape='point')
    for state in dfa.accept_states:
        dot.node(str(id(state)), peripheries='2')
    for state in dfa.states:
        dot.node(str(id(state)))
        if state == dfa.start_state:
            dot.edge(str(id(dfa.start_state)), str(id(state)), label='')
        for symbol, next_state in state.transitions.items():
            dot.edge(str(id(state)), str(id(next_state)), label=symbol)
    dot.render('dfa.gv', view=True)

def minimize_dfa(dfa):
    accepting_states = set()
    non_accepting_states = set()
    for state in dfa.states:
        if state in dfa.accept_states:
            accepting_states.add(state)
        else:
            non_accepting_states.add(state)

    partitions = [accepting_states, non_accepting_states]
    queue = [accepting_states, non_accepting_states]

    while queue:
        p = queue.pop(0)
        for symbol in dfa.symbols():
            x = set()
            for state in p:
                x.add(state.transitions.get(symbol, None))

            new_partitions = []
            for partition in partitions:
                y = partition.intersection(x)
                z = partition.difference(x)
                if y and z:
                    new_partitions.append(y)
                    new_partitions.append(z)
                else:
                    new_partitions.append(partition)

            if len(new_partitions) > len(partitions):
                partitions = new_partitions
                queue.append(y)
                queue.append(z)

    dfa_states = []
    dfa_transitions = {}

    for partition in partitions:
        dfa_state = DFAState(set())
        for state in partition:
            dfa_state.nfa_states.update(state.nfa_states)

        dfa_states.append(dfa_state)

    for dfa_state in dfa_states:
        for symbol in dfa.symbols():
            next_states = set()
            for state in dfa_state.nfa_states:
                next_states.update(state.transitions.get(symbol, set()))
            for partition in partitions:
                if next_states.issubset(partition):
                    next_dfa_state = None
                    for state in dfa_states:
                        if state.nfa_states == next_states:
                            next_dfa_state = state
                            break
                    if not next_dfa_state:
                        next_dfa_state = DFAState(next_states)
                        dfa_states.append(next_dfa_state)
                    dfa_state.transitions[symbol] = next_dfa_state

    new_dfa = DFA(dfa_states[0], set())
    for dfa_state in dfa_states:
        if dfa_state.nfa_states.intersection(dfa.accept_states):
            new_dfa.accept_states.add(dfa_state)
        new_dfa.add_state(dfa_state)

    return new_dfa


def nfa_accepts_string(nfa, string):
    current_states = nfa.epsilon_closure(nfa.start_state)
    for symbol in string:
        next_states = nfa.move(current_states, symbol)
        current_states = set()
        for state in next_states:
            current_states.update(nfa.epsilon_closure(state))
    return any(state == nfa.end_state for state in current_states)

def dfa_accepts_string(dfa, string):
    current_state = dfa.start_state
    for symbol in string:
        if symbol not in current_state.transitions:
            return False
        current_state = current_state.transitions[symbol]
    return current_state in dfa.accept_states

