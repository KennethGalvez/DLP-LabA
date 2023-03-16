from pythomata.automata import Automaton 
from pythomata.algorithms.to_automaton import to_automaton


# Definimos una función que convierte una expresión postfix en un AFN
def postfix_to_nfa(postfix):
    stack = []
    for c in postfix:
        if c == '.':
            # Concatenación
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            nfa1.concatenate(nfa2)
            stack.append(nfa1)
        elif c == '|':
            # Unión
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            nfa1.union(nfa2)
            stack.append(nfa1)
        elif c == '*':
            # Cierre de Kleene
            nfa = stack.pop()
            nfa.kleene_star()
            stack.append(nfa)
        else:
            # Carácter
            nfa = Automaton()
            nfa.add_transition(nfa.initial_state, nfa.create_state(), c)
            nfa.add_final_state(nfa.initial_state)
            stack.append(nfa)
    return stack.pop()

# Definimos una función que utiliza el algoritmo de construcción de subconjuntos para convertir un AFN en un AFD
def nfa_to_dfa(nfa):
    dfa = to_automaton(nfa).minimize()
    return dfa

# Ejemplo de uso
postfix = "ab|c*."
nfa = postfix_to_nfa(postfix)
dfa = nfa_to_dfa(nfa)

# Mostramos los autómatas resultantes
print("AFN resultante:")
print(nfa.to_dot())
print("AFD resultante:")
print(dfa.to_dot())
