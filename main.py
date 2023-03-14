from postfix import *
from nfa import *

# Uso del programa

expresion_regular = '(a|b)*c'
expresion_postfix = infix_a_postfix(expresion_regular)
nfa = postfix_to_nfa(expresion_postfix)
visualize_nfa(nfa)


if expresion_postfix is not None:
    print(f"La expresión regular {expresion_regular} en notación postfix es: {expresion_postfix}")
else:
    print(f"La expresión regular {expresion_regular} es inválida.")



#nfa = postfix_to_nfa()
#visualize_nfa(nfa)

