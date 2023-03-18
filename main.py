from postfix import *
from nfa import *
from AFD import *
from Direc import *

# Uso del programa
expresion_regular = '(a|b)c*'
expresion_postfix = infix_a_postfix(expresion_regular)

nfa = postfix_to_nfa(expresion_postfix)


dfa = nfa_to_dfa(nfa)

#print(nfa_accepts_string(nfa, 'a'))  
#print(dfa_accepts_string(nfa, 'a'))  

#print_dfa(dfa)
#graph(dfa)

min = minimize_dfa(dfa)

#print_dfa(min)
#graph(min)

#dfad = construir_afd(expresion_regular)
#dfa_min = minimizar_dfa(dfa)
#print(dfa_min.to_dot())


#if expresion_postfix is not None:
#    print(f"La expresión regular {expresion_regular} en notación postfix es: {expresion_postfix}")
#else:
#    print(f"La expresión regular {expresion_regular} es inválida.")

# nfa = postfix_to_nfa(expresion_postfix)
# visualize_nfa(nfa)



