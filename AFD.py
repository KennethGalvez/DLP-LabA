class State:
    """
    Clase para representar un estado en un automata finito no determinista.
    """
    def __init__(self, label=None, edges=None):
        self.label = label
        self.edges = edges or []

class NFA:
    """
    Clase para representar un automata finito no determinista.
    """
    def __init__(self, start=None, end=None):
        self.start = start
        self.end = end

    def connect(self, state):
        """
        Conecta el estado inicial del NFA con el estado proporcionado.
        """
        self.start.edges.append(state)

    def merge(self, nfa):
        """
        Fusiona este NFA con otro NFA proporcionado.
        """
        self.end.edges.append(nfa.start)
        self.end = nfa.end
    
    def get_alphabet(self):
        """
        Obtiene el alfabeto del NFA.
        """
        alphabet = set()
        for state in self.get_states():
            for edge in state.edges:
                if edge.label is not None:
                    alphabet.add(edge.label)
        return alphabet


def postfix_to_nfa(postfix):
    """
    Convierte una expresión postfix en un NFA.
    """
    stack = []

    for c in postfix:
        if c == '.':
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            nfa1.merge(nfa2)
            stack.append(nfa1)
        elif c == '|':
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            start = State()
            end = State()
            start.edges.append(nfa1.start)
            start.edges.append(nfa2.start)
            nfa1.end.edges.append(end)
            nfa2.end.edges.append(end)
            stack.append(NFA(start, end))
        elif c == '*':
            nfa = stack.pop()
            start = State()
            end = State()
            start.edges.append(nfa.start)
            start.edges.append(end)
            nfa.end.edges.append(nfa.start)
            nfa.end.edges.append(end)
            stack.append(NFA(start, end))
        else:
            state = State()
            state.label = c
            stack.append(NFA(state, state))

    return stack.pop()

from graphviz import Digraph, render

class DFAState:
    """
    Clase para representar un estado en un automata finito determinista.
    """
    def __init__(self, states=None):
        self.states = states or []
        self.transitions = {}

    def add_transition(self, symbol, state):
        """
        Agrega una transición para el símbolo especificado al estado proporcionado.
        """
        self.transitions[symbol] = state

class DFA:
    """
    Clase para representar un automata finito determinista.
    """
    def __init__(self, start=None, states=None):
        self.start = start
        self.states = states or []

def epsilon_closure(states):
    """
    Calcula el conjunto de estados alcanzables desde los estados proporcionados por transiciones epsilon.
    """
    closure = set(states)
    queue = list(states)
    while queue:
        state = queue.pop(0)
        for edge in state.edges:
            if edge.label is None and edge not in closure:
                closure.add(edge)
                queue.append(edge)
    return closure

def move(states, symbol):
    """
    Calcula el conjunto de estados alcanzables desde los estados proporcionados por transiciones que corresponden al símbolo especificado.
    """
    move_states = set()
    for state in states:
        for edge in state.edges:
            if edge.label == symbol:
                move_states.add(edge)
    return move_states

def nfa_to_dfa(nfa):
    """
    Convierte un NFA en un DFA utilizando el algoritmo de construcción de subconjuntos.
    """
    # Obtenemos el alfabeto del NFA
    alphabet = nfa.get_alphabet()

    # Creamos el estado inicial del DFA
    start = frozenset(nfa.epsilon_closure({nfa.start}))

    # Inicializamos el conjunto de estados y las transiciones del DFA
    states = set()
    transitions = {}

    # Agregamos el estado inicial al conjunto de estados del DFA
    states.add(start)

    # Procesamos los estados del DFA hasta que no haya más estados nuevos por agregar
    pending = [start]
    while pending:
        state = pending.pop(0)

        # Para cada símbolo del alfabeto, calculamos el conjunto de estados alcanzables desde el estado actual
        for symbol in alphabet:
            next_state = frozenset(nfa.epsilon_closure(nfa.move(state, symbol)))

            # Si el conjunto de estados resultante no está vacío, lo agregamos al conjunto de estados del DFA
            if next_state:
                transitions[(state, symbol)] = next_state
                if next_state not in states:
                    states.add(next_state)
                    pending.append(next_state)

    # Identificamos los estados de aceptación del DFA
    accept_states = set()
    for state in states:
        for nfa_state in state:
            if nfa_state in nfa.accept_states:
                accept_states.add(state)

    # Creamos y devolvemos el DFA resultante
    return DFA(states, alphabet, transitions, start, accept_states)


def draw_dfa(dfa, filename='dfa'):
    """
    Crea una imagen del grafo correspondiente al AFD proporcionado usando la biblioteca graphviz.
    """
    dot = Digraph(comment='DFA')
    dot.attr(rankdir='LR')
    dot.attr('node', shape='circle')
    dot.attr('edge', arrowhead='vee')

    # Agregamos los estados
    for state in dfa.states:
        if state == dfa.start:
            dot.attr('node', shape='doublecircle')
            dot.node(str(state))
            dot.attr('node', shape='circle')
        elif state in dfa.accept_states:
            dot.attr('node', peripheries='2')
            dot.node(str(state))
            dot.attr('node', peripheries='1')
        else:
            dot.node(str(state))

    # Agregamos las transiciones
    for state in dfa.states:
        for symbol, next_state in state.transitions.items():
            dot.edge(str(state), str(next_state), label=symbol)

    dot.render(filename, view=True)

