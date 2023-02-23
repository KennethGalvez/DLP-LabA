from graphviz import Digraph
from collections import defaultdict

# Definir la precedencia de los operadores
precedence = {'*': 3, '+': 2, '.': 1}

def infix_to_postfix(infix):
    # Inicializar una pila y una lista de salida vacías
    stack = []
    output = []
    # Convertir la expresión en una lista de tokens
    tokens = list(infix)

    for token in tokens:
        if token.isalpha() or token.isdigit():
            # Si el token es un carácter o un dígito, agregarlo a la lista de salida
            output.append(token)
        elif token in '*+.':
            # Si el token es un operador, sacar los operadores de mayor o igual precedencia de la pila y agregarlos a la lista de salida
            while stack and stack[-1] != '(' and precedence[token] <= precedence.get(stack[-1], 0):
                output.append(stack.pop())
            # Agregar el operador a la pila
            stack.append(token)
        elif token == '(':
            # Si el token es un paréntesis izquierdo, agregarlo a la pila
            stack.append(token)
        elif token == ')':
            # Si el token es un paréntesis derecho, sacar los operadores de la pila y agregarlos a la lista de salida hasta que se encuentre el paréntesis izquierdo correspondiente
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            # Sacar el paréntesis izquierdo de la pila
            stack.pop()

    # Sacar los operadores restantes de la pila y agregarlos a la lista de salida
    while stack:
        output.append(stack.pop())

    # Convertir la lista de salida en una cadena y devolverla
    return ''.join(output)

infix_regex = '(a+b)*.c'
postfix_regex = infix_to_postfix(infix_regex)

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
        self.transitions = defaultdict(lambda: defaultdict(set))
        
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
        elif symbol == '.':
            if len(stack) < 2:
                raise ValueError("Invalid regular expression")
            second_state = stack.pop()
            first_state = stack[-1]
            first_state.add_epsilon_transition(second_state)
        elif symbol == '?':
            if len(stack) < 1:
                raise ValueError("Invalid regular expression")
            state = State()
            state.add_epsilon_transition(stack[-1])
            state.add_epsilon_transition(State())
            stack[-1] = state

    accept_state = stack.pop()
    start_state = State()
    start_state.add_epsilon_transition(accept_state)

    return NFA(start_state, set([accept_state]))

def visualize_nfa(nfa):
    dot = Digraph(comment='NFA')

    for state in nfa.transitions.keys():
        dot.node(str(state), shape='circle')
        if state in nfa.accept_states:
            dot.node(str(state), shape='doublecircle')

    dot.node('start', shape='point')
    dot.edge('start', str(nfa.start_state))

    for state in nfa.transitions.keys():
        for symbol in nfa.transitions[state]:
            for destination in nfa.transitions[state][symbol]:
                dot.edge(str(state), str(destination), label=symbol)

    dot.render('nfa.gv', view=True)

nfa = postfix_to_nfa(postfix_regex)
visualize_nfa(nfa)
