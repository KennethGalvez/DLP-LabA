from graphviz import Digraph

class State:
    id_counter = 0
    def __init__(self, label=None):
        State.id_counter += 1
        self.id = State.id_counter
        self.label = label if label is not None else str(self.id)
        self.transitions = {}

class NFA:
    def __init__(self, start_state, accept_states):
        self.start_state = start_state
        self.accept_states = accept_states

    def get_states(self):
        states = [self.start_state] + self.accept_states
        for state in states:
            states.extend(state.transitions.values())
        return list(set(states))

def postfix_to_nfa(postfix):
    stack = []
    for c in postfix:
        if c == '|':
            nfa1 = stack.pop()
            nfa2 = stack.pop()
            accept_state = State()
            start_state = State(transitions={None: nfa2.start_state, None: nfa1.start_state})
            nfa2.accept_states[0].transitions[None] = accept_state
            nfa1.accept_states[0].transitions[None] = accept_state
            stack.append(NFA(start_state, [accept_state]))
        elif c == '*':
            nfa = stack.pop()
            accept_state = State()
            start_state = State(transitions={None: nfa.start_state, None: accept_state})
            nfa.accept_states[0].transitions[None] = nfa.start_state
            nfa.accept_states[0].transitions[None] = accept_state
            stack.append(NFA(start_state, [accept_state]))
        elif c == '+':
            nfa = stack.pop()
            accept_state = State()
            start_state = State(transitions={None: nfa.start_state})
            nfa.accept_states[0].transitions[None] = start_state
            nfa.accept_states[0].transitions[None] = accept_state
            stack.append(NFA(start_state, [accept_state]))
        elif c == '?':
            nfa = stack.pop()
            accept_state = State()
            start_state = State(transitions={None: nfa.start_state, None: accept_state})
            nfa.accept_states[0].transitions[None] = accept_state
            stack.append(NFA(start_state, [accept_state]))
        else:
            accept_state = State()
            start_state = State(transitions={c: accept_state})
            stack.append(NFA(start_state, [accept_state]))

    return stack.pop()

def nfa_to_dot(nfa):
    dot = Digraph()
    states = nfa.get_states()
    for state in states:
        dot.node(str(state.id), state.label, shape='circle')
    dot.node('start', '', shape='none')
    dot.edge('start', str(nfa.start_state.id))
    for accept_state in nfa.accept_states:
        dot.node(str(accept_state.id), '', shape='doublecircle')
    for state in states:
        for symbol, next_state in state.transitions.items():
            if symbol is None:
                symbol = 'ε'
            dot.edge(str(state.id), str(next_state.id), label=symbol)
    return dot

def postfix_to_dot(postfix):
    nfa = postfix_to_nfa(postfix)
    return nfa_to_dot(nfa)

if __name__ == '__main__':
    postfix = 'ab|c*'
    nfa = postfix_to_nfa(postfix)
    dot = nfa_to_dot(nfa)
    dot.render('nfa.gv', view=True)
