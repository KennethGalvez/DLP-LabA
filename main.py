from postfix import *
from nfa import *

# Uso del programa
# expresion_regular = '(a|b)*c'
# expresion_postfix = infix_a_postfix(expresion_regular)
# if expresion_postfix is not None:
#     print(f"La expresión regular {expresion_regular} en notación postfix es: {expresion_postfix}")
# else:
#     print(f"La expresión regular {expresion_regular} es inválida.")

# nfa = postfix_to_nfa(expresion_postfix)
# visualize_nfa(nfa)

from AFD import postfix_to_nfa, nfa_to_dfa, draw_dfa

# Convertimos una expresión postfix en un NFA
nfa = postfix_to_nfa('ab.c*.')

# Convertimos el NFA en un AFD
dfa = nfa_to_dfa(nfa)

# Dibujamos el AFD como un grafo
draw_dfa(dfa, filename='ejemplo')


