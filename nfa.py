from graphviz import Digraph

class State:
    state_counter = 0

    def __init__(self, accept_state=False):
        self.accept_state = accept_state
        self.transitions = {}
        self.id = State.state_counter
        State.state_counter += 1

    def add_transition(self, symbol, state):
        if symbol not in self.transitions:
            self.transitions[symbol] = []
        self.transitions[symbol].append(state)

class NFA:
    def __init__(self, start_state, accept_state):
        self.start_state = start_state
        self.accept_state = accept_state

    def get_states(self):
        visited = set()
        states = []

        def dfs(state):
            if state in visited:
                return
            visited.add(state)
            states.append(state)
            for transitions in state.transitions.values():
                for next_state in transitions:
                    dfs(next_state)

        dfs(self.start_state)
        return states

def postfix_to_nfa(expression):
    stack = []
    for char in expression:
        if char == '|':
            right = stack.pop()
            left = stack.pop()
            new_start_state = State()
            new_start_state.add_transition('ε', left.start_state)
            new_start_state.add_transition('ε', right.start_state)
            new_accept_state = State(accept_state=True)
            left.accept_state.add_transition('ε', new_accept_state)
            right.accept_state.add_transition('ε', new_accept_state)
            stack.append(NFA(new_start_state, new_accept_state))
        elif char == '*':
            nfa = stack.pop()
            new_start_state = State()
            new_accept_state = State(accept_state=True)
            new_start_state.add_transition('ε', nfa.start_state)
            new_start_state.add_transition('ε', new_accept_state)
            nfa.accept_state.add_transition('ε', nfa.start_state)
            nfa.accept_state.add_transition('ε', new_accept_state)
            stack.append(NFA(new_start_state, new_accept_state))
        elif char == '.':
            right = stack.pop()
            left = stack.pop()
            left.accept_state.add_transition('ε', right.start_state)
            stack.append(NFA(left.start_state, right.accept_state))
        else:
            state1 = State()
            state2 = State(accept_state=True)
            state1.add_transition(char, state2)
            stack.append(NFA(state1, state2))

    nfa = stack.pop()
    return nfa

def visualize_nfa(nfa):
    graph = Digraph(format='png')

    states = nfa.get_states()

    for state in states:
        if state.accept_state:
            graph.node(str(state.id), shape='doublecircle')
        else:
            graph.node(str(state.id), shape='circle')

    graph.edge('', str(nfa.start_state.id))

    for state in states:
        for symbol, transitions in state.transitions.items():
            for next_state in transitions:
                graph.edge(str(state.id), str(next_state.id), label=symbol)

    graph.render('nfa', view=True)
