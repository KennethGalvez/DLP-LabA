from postfix import infix_to_postfix
from nfa import postfix_to_nfa, visualize_nfa

# Uso del programa
infix_regex = '' 
#infix_regex = '(a'
postfix_regex = infix_to_postfix(infix_regex)
nfa = postfix_to_nfa(postfix_regex)
visualize_nfa(nfa)

