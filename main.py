from postfix import infix_to_postfix
from nfa import postfix_to_nfa, visualize_nfa

# Ejemplo de uso
infix_regex = '(a|b)*c' 
#infix_regex = '(a?'
postfix_regex = infix_to_postfix(infix_regex)
nfa = postfix_to_nfa(postfix_regex)
visualize_nfa(nfa)

# print("Estado inicial:", nfa.start_state.number)
# print("Estados de aceptación:", [s.number for s in nfa.accept_states])
# for state in range(State.count):
#     s = State()
# print("Estado", state, ":", s.transitions, s.epsilon_transitions)