import json
from graphviz import Digraph

# Definimos la clase Node para representar los nodos del AFN
class Node:
    def __init__(self, left=None, right=None, label=None, id=None):
        self.left = left
        self.right = right
        self.label = label
        self.id = id

# Definimos la clase NFA para representar el AFN
class NFA:
    def __init__(self, start=None, accept=None):
        self.start = start
        self.accept = accept

    # Función para generar el grafo del AFN en formato JSON
    def to_graph(self):
        graph = {}
        queue = [self.start]
        node_id = 0
        while queue:
            node = queue.pop(0)
            if node.id is None:
                node.id = node_id
                node_id += 1
            if node.label is not None:
                graph[node.id] = {'label': node.label, 'edges': []}
            if node.left is not None:
                graph[node.id] = {'label': None, 'edges': []}
                graph[node.left.id] = {'label': None, 'edges': []}
                graph[node.id]['edges'].append({'to': node.left.id, 'label': 'ε'})
                queue.append(node.left)
            if node.right is not None:
                graph[node.right.id] = {'label': None, 'edges': []}
                graph[node.id]['edges'].append({'to': node.right.id, 'label': 'ε'})
                queue.append(node.right)
            if node.edge is not None:
                graph[node.edge.id] = {'label': None, 'edges': []}
                graph[node.id]['edges'].append({'to': node.edge.id, 'label': node.label})
                queue.append(node.edge)
            if node.edge2 is not None:
                graph[node.edge2.id] = {'label': None, 'edges': []}
                graph[node.id]['edges'].append({'to': node.edge2.id, 'label': 'ε'})
                queue.append(node.edge2)
        return graph

# Definimos la función que convierte una expresión regular en notación infix a notación postfix
def infix_to_postfix(infix):
    # Definimos los operadores y sus precedencias
    operators = {'*': 100, '.': 80, '|': 60, '(': 40, ')': 20}
    # Creamos una pila para almacenar los operadores
    stack = []
    # Creamos una lista para almacenar la expresión en notación postfix
    postfix = []
    # Dividimos la expresión infix en tokens
    tokens = infix.split()
    # Recorremos los tokens de izquierda a derecha
    for token in tokens:
        if token.isalpha():
            postfix.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack[-1] != '(':
                postfix.append(stack.pop())
            stack.pop()
        else:
            while stack and operators.get(stack[-1], 0) >= operators.get(token, 0):
                postfix.append(stack.pop())
            stack.append(token)
    while stack:
        postfix.append(stack.pop())
    return ' '.join(postfix)

# Definimos la función que convierte una expresión regular en notación postfix en un AFN
def regex_to_nfa(regex):
    # Creamos una pila para almacenar los fragmentos de AFN
    stack = []
    # Dividimos la expresión postfix en tokens
    tokens = regex.split()
    # Recorremos los tokens de izquierda a derecha
    for token in tokens:
        if token.isalpha():
            # Si el token es un símbolo del alfabeto, creamos un fragmento de AFN básico
            accept = Node(label=token)
            start = Node(edge=accept)
            stack.append(NFA(start=start, accept=accept))
        elif token == '*':
            # Si el token es un operador de cierre de Kleene, aplicamos la operación a un fragmento de AFN
            nfa = stack.pop()
            accept = nfa.accept
            start = Node(edge=nfa.start)
            accept.edge = nfa.start
            start2 = Node(edge=start)
            accept2 = Node(edge=start)
            stack.append(NFA(start=start2, accept=accept2))
        elif token == '.':
            # Si el token es un operador de concatenación, concatenamos dos fragmentos de AFN
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            nfa1.accept.edge = nfa2.start
            stack.append(NFA(start=nfa1.start, accept=nfa2.accept))
        elif token == '|':
            # Si el token es un operador de unión, unimos dos fragmentos de AFN
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            start = Node(edge=nfa1.start)
            start.edge2 = nfa2.start
            accept = Node()
            nfa1.accept.edge = accept
            nfa2.accept.edge = accept
            stack.append(NFA(start=start, accept=accept))

    # El último elemento en la pila es el AFN completo
    nfa = stack.pop()

    # Generamos el grafo del AFN en formato JSON
    graph = nfa.to_graph()
    with open('nfa.json', 'w') as f:
        json.dump(graph, f)

    # Dibujamos el diagrama de transición de estados del autómata utilizando la biblioteca graphviz
    dot = Digraph(comment='NFA')
    for node_id in graph:
        label = graph[node_id]['label'] if graph[node_id]['label'] is not None else ''
        shape = 'doublecircle' if node_id == nfa.accept.id else 'circle'
        dot.node(str(node_id), label=label, shape=shape)
    for node_id in graph:
        for edge in graph[node_id]['edges']:
            dot.edge(str(node_id), str(edge['to']), label=edge['label'])
    dot.render('nfa', view=True)
    
    return nfa

# Ejemplo de uso
r = '( a | b )* c'
r_postfix = infix_to_postfix(r)
nfa = regex_to_nfa(r_postfix)