class State:
    def __init__(self, label=None):
        self.transitions = {}
        self.label = label
        self.final = False

class NFA:
    def __init__(self, start=None, end=None):
        self.start = start
        self.end = end

def postfix_to_nfa(postfix):
    stack = []
    for c in postfix:
        if c == '.':
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            nfa1.end.transitions[''] = nfa2.start
            stack.append(NFA(nfa1.start, nfa2.end))
        elif c == '|':
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            start = State()
            start.transitions[''] = nfa1.start
            start.transitions[''] = nfa2.start
            end = State()
            nfa1.end.transitions[''] = end
            nfa2.end.transitions[''] = end
            stack.append(NFA(start, end))
        elif c == '*':
            nfa = stack.pop()
            start = State()
            end = State()
            start.transitions[''] = nfa.start
            start.transitions[''] = end
            nfa.end.transitions[''] = nfa.start
            nfa.end.transitions[''] = end
            stack.append(NFA(start, end))
        else:
            state = State(c)
            stack.append(NFA(state, state))
    nfa = stack.pop()
    nfa.end.final = True
    return nfa

def get_states(nfa):
    states = set()
    queue = [nfa.start]
    while queue:
        state = queue.pop()
        if state in states:
            continue
        states.add(state)
        for symbol, next_state in state.transitions.items():
            queue.append(next_state)
    return states

def get_alphabet(nfa):
    alphabet = set()
    for state in get_states(nfa):
        for symbol in state.transitions.keys():
            if symbol:
                alphabet.add(symbol)
    return alphabet

def get_transitions(nfa):
    transitions = {}
    for state in get_states(nfa):
        for symbol, next_state in state.transitions.items():
            if not symbol:
                symbol = 'epsilon'
            if state not in transitions:
                transitions[state] = {}
            if symbol not in transitions[state]:
                transitions[state][symbol] = set()
            transitions[state][symbol].add(next_state)
    return transitions

def print_transition_table(nfa):
    def state_cmp(s1, s2):
        if s1.label is None and s2.label is None:
            return 0
        elif s1.label is None:
            return -1
        elif s2.label is None:
            return 1
        else:
            return int(s1.label) - int(s2.label)

    states = sorted(list(get_states(nfa)), key=lambda s: (s.label is None, s.label))
    alphabet = sorted(list(get_alphabet(nfa)))
    transitions = get_transitions(nfa)

    print('{:<10}'.format(''), end='')
    for symbol in alphabet:
        print('{:<10}'.format(symbol), end='')
    print('')

    for state in states:
        print('{:<10}'.format(state.label if state.label is not None else 'epsilon'), end='')
        for symbol in alphabet:
            next_states = transitions[state][symbol] if symbol in transitions[state] else set()
            labels = ', '.join(sorted([s.label for s in next_states if s.label is not None]))
            print('{:<10}'.format(labels), end='')
        print('')


# Ejemplo de uso
postfix_expression = 'a*b*|c'
nfa = postfix_to_nfa(postfix_expression)
print_transition_table(nfa)
