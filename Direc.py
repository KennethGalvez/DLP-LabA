from graphviz import Digraph

class Estado:
    def __init__(self, nombre, aceptacion=False):
        self.nombre = nombre
        self.transiciones = {}
        self.aceptacion = aceptacion
    
    def agregar_transicion(self, simbolo, estado_destino):
        if simbolo not in self.transiciones:
            self.transiciones[simbolo] = []
        self.transiciones[simbolo].append(estado_destino)
    
    def transiciones_para(self, simbolo):
        return self.transiciones.get(simbolo, [])

class Automata:
    def __init__(self, estado_inicial, estado_aceptacion):
        self.estado_inicial = estado_inicial
        self.estado_aceptacion = estado_aceptacion
        self.transiciones_dict = {}

        
    def acepta(self, cadena):
        estado_actual = self.estado_inicial
        for simbolo in cadena:
            if simbolo not in estado_actual.transiciones:
                return False
            estado_actual = estado_actual.transiciones_para(simbolo)[0]
        return estado_actual.aceptacion
    
    def estados(self):
        estados = []
        por_revisar = [self.estado_inicial]
        while por_revisar:
            estado = por_revisar.pop()
            if estado in estados:
                continue
            estados.append(estado)
            for destino in estado.transiciones.values():
                por_revisar.extend(destino)
        return estados
    
    def transiciones(self):
        for estado in self.estados():
            for simbolo, destinos in estado.transiciones.items():
                for destino in destinos:
                    self.transiciones_dict[(estado, simbolo)] = destino
        return self.transiciones_dict
    
    def to_dot(self):
        dot = Digraph()
        dot.attr('node', shape='circle')
        for estado in self.estados():
            attrs = {'shape': 'doublecircle'} if estado.aceptacion else {}
            dot.node(str(estado), **attrs)
        dot.node('inicial', shape='point')
        dot.edge('inicial', str(self.estado_inicial))
        for origen, simbolo in self.transiciones_dict.keys():
            dot.edge(str(origen), str(self.transiciones_dict[(origen, simbolo)]), label=simbolo)
        
        dot.format = 'png'
        dot.render('automata')

        return dot.source

def construir_afd(expresion_regular):
    pila = []
    for simbolo in expresion_regular:
        if simbolo == '|':
            derecha = pila.pop()
            izquierda = pila.pop()
            nuevo_inicial = Estado('q')
            nuevo_inicial.agregar_transicion('e', izquierda.estado_inicial)
            nuevo_inicial.agregar_transicion('e', derecha.estado_inicial)
            nuevo_aceptacion = Estado('q', True)
            izquierda.estado_aceptacion.agregar_transicion('e', nuevo_aceptacion)
            derecha.estado_aceptacion.agregar_transicion('e', nuevo_aceptacion)
            pila.append(Automata(nuevo_inicial, nuevo_aceptacion))
        elif simbolo == '.':
            derecha = pila.pop()
            izquierda = pila.pop()
            izquierda.estado_aceptacion.agregar_transicion('e', derecha.estado_inicial)
            pila.append(Automata(izquierda.estado_inicial, derecha.estado_aceptacion))
        elif simbolo == '*':
            automata = pila.pop()
            nuevo_inicial = Estado('q')
            nuevo_aceptacion = Estado('q', True)
            nuevo_inicial.agregar_transicion('e', automata.estado_inicial)
            automata.estado_aceptacion.agregar_transicion('e', nuevo_aceptacion)
            nuevo_inicial.agregar_transicion('e', nuevo_aceptacion)
            automata.estado_aceptacion.agregar_transicion('e', automata.estado_inicial)
            pila.append(Automata(nuevo_inicial, nuevo_aceptacion))
        else:
            nuevo_estado = Estado('q')
            nuevo_aceptacion = Estado('q', True)
            nuevo_estado.agregar_transicion(simbolo, nuevo_aceptacion)
            pila.append(Automata(nuevo_estado, nuevo_aceptacion))

    dfa = pila.pop()
    print(dfa.to_dot())  # Display the DFA graph
    return dfa


def minimizar_dfa(dfa):
    # Create the initial partition, which consists of two groups: the accepting states, and the non-accepting states
    aceptacion = [estado for estado in dfa.estados() if estado.aceptacion]
    no_aceptacion = [estado for estado in dfa.estados() if not estado.aceptacion]
    particion_actual = [aceptacion, no_aceptacion]
    
    # Keep track of which partition each state belongs to
    estados_a_particiones = {}
    for i, particion in enumerate(particion_actual):
        for estado in particion:
            estados_a_particiones[estado] = i
    
    # Keep refining the partition until it no longer changes
    while True:
        nuevas_particiones = []
        for particion in particion_actual:
            nuevas_subparticiones = {}
            for estado in particion:
                transiciones = estado.transiciones
                subparticion_key = tuple(estados_a_particiones[transicion] for simbolo, transiciones in transiciones.items() for transicion in transiciones)
                if subparticion_key not in nuevas_subparticiones:
                    nuevas_subparticiones[subparticion_key] = []
                nuevas_subparticiones[subparticion_key].append(estado)
            nuevas_particiones.extend(nuevas_subparticiones.values())
        
        if nuevas_particiones == particion_actual:
            break
        
        particion_actual = nuevas_particiones
        for i, particion in enumerate(particion_actual):
            for estado in particion:
                estados_a_particiones[estado] = i
    
    # Create a new set of states for the minimized DFA
    nuevo_estados = []
    nuevo_a_particiones = {}
    for i, particion in enumerate(particion_actual):
        nuevo_estado = Estado(str(i), any(estado.aceptacion for estado in particion))
        nuevo_estados.append(nuevo_estado)
        for estado in particion:
            nuevo_a_particiones[estado] = nuevo_estado
    
    # Add transitions to the new states
    for estado in dfa.estados():
        for simbolo, destinos in estado.transiciones.items():
            nuevo_origen = nuevo_a_particiones[estado]
            nuevo_destino = nuevo_a_particiones[destinos[0]]
            nuevo_origen.agregar_transicion(simbolo, nuevo_destino)
    
    # Find the new initial and accepting states
    nuevo_estado_inicial = nuevo_a_particiones[dfa.estado_inicial]
    nuevo_estado_aceptacion = None
    for estado in nuevo_estados:
        if estado.aceptacion:
            nuevo_estado_aceptacion = estado
            break
    
    # Create and return the minimized DFA
    return Automata(nuevo_estado_inicial, nuevo_estado_aceptacion)


#dfa = construir_afd('(a|b)*')
#dfa_min = minimizar_dfa(dfa)
#print(dfa_min.to_dot())
