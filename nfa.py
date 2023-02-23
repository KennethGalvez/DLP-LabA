from graphviz import Digraph

class State:
    """Representa un estado en un autómata finito no determinista."""

    count = 0

    def __init__(self):
        """Inicializa un nuevo estado."""
        self.transitions = {}
        self.epsilon_transitions = set()
        self.number = State.count
        State.count += 1

    def add_transition(self, symbol, state):
        """Agrega una transición del estado actual al estado dado con el símbolo dado."""
        if symbol not in self.transitions:
            self.transitions[symbol] = set()
        self.transitions[symbol].add(state)

    def add_epsilon_transition(self, state):
        """Agrega una transición épsilon del estado actual al estado dado."""
        self.epsilon_transitions.add(state)

class NFA:
    """Representa un autómata finito no determinista."""

    def __init__(self, start_state, accept_states):
        """Inicializa un nuevo autómata finito no determinista con el estado inicial y los estados de aceptación dados."""
        self.start_state = start_state
        self.accept_states = accept_states
        
    def match(self, string):
        """Determina si el autómata acepta la cadena dada."""
        current_states = set([self.start_state])
        for symbol in string:
            next_states = set()
            for state in current_states:
                if symbol in state.transitions:
                    next_states.update(state.transitions[symbol])
            current_states = next_states
        return any(state in self.accept_states for state in current_states)

def postfix_to_nfa(postfix_regex):
    stack = []
    for symbol in postfix_regex:
        if symbol.isalpha() or symbol.isdigit():
            state = State()
            state.add_transition(symbol, State())
            stack.append(state)
        elif symbol == '*':
            if len(stack) < 1:
                raise ValueError("Invalid regular expression")
            state = State()
            state.add_epsilon_transition(stack[-1])
            stack[-1].add_epsilon_transition(state)
            stack[-1] = state
        elif symbol == '+':
            if len(stack) < 2:
                raise ValueError("Invalid regular expression")
            second_state = stack.pop()
            first_state = stack[-1]
            state = State()
            state.add_epsilon_transition(first_state)
            state.add_epsilon_transition(second_state)
            stack[-1] = state
        elif symbol == '?':
            if len(stack) < 1:
                raise ValueError("Invalid regular expression")
            state = State()
            state.add_epsilon_transition(stack[-1])
            state.add_epsilon_transition(State())
            stack[-1] = state
        elif symbol == '':
            if len(stack) < 2:
                raise ValueError("Invalid regular expression")
            second_state = stack.pop()
            first_state = stack[-1]
            for c in second_state.transitions.keys():
                first_state.add_transition(c, second_state.transitions[c])
            for s in second_state.epsilon_transitions:
                first_state.add_epsilon_transition(s)

    accept_state = stack.pop()
    start_state = State()
    start_state.add_epsilon_transition(accept_state)

    return NFA(start_state, set([accept_state]))

def visualize_nfa(nfa):
    dot = Digraph(comment='NFA')

    # Agregar los nodos del autómata
    for state in nfa.start_state.epsilon_transitions:
        dot.node(str(state.number), shape='circle', style='bold')
    dot.node(str(nfa.start_state.number), shape='doublecircle', style='bold')

    # Agregar los arcos del autómata
    for state in nfa.start_state.epsilon_transitions:
        visualize_nfa_rec(dot, state, set())
    
    print(dot.source)
    dot.render('nfa.gv', view=True)
    
def visualize_nfa_rec(dot, state, visited):
    visited.add(state)

    for symbol, transitions in state.transitions.items():
        for transition in transitions:
            dot.edge(str(state.number), str(transition.number), label=symbol)

            if transition not in visited:
                visualize_nfa_rec(dot, transition, visited)

    for transition in state.epsilon_transitions:
        dot.edge(str(state.number), str(transition.number), label='ε')

        if transition not in visited:
            visualize_nfa_rec(dot, transition, visited)
