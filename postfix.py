def infix_a_postfix(expresion):
    precedencia = {'*': 3, '+': 3, '|': 2, '.': 1, '(': 0, ')': 0}
    salida = []
    pila_operadores = []

    for i, c in enumerate(expresion):
        if c.isalpha():
            salida.append(c)
        elif c == '(':
            pila_operadores.append(c)
        elif c == ')':
            while pila_operadores and pila_operadores[-1] != '(':
                salida.append(pila_operadores.pop())
            if not pila_operadores or pila_operadores[-1] != '(':
                # Paréntesis desequilibrados
                return None
            # Eliminar el paréntesis izquierdo de la pila de operadores
            pila_operadores.pop()
        elif c in {'*', '+', '|', '.'}:
            if i == len(expresion) - 1 and c != '*' and c != '+':
                # Operador final inválido
                return None
            if c == '+' and (not pila_operadores or pila_operadores[-1] not in {'|', '.'}):
                # Error: el operador + debe aplicarse a un símbolo o una expresión regular válida
                return "Error en la expresión regular ingresada. El operador + no se está aplicando a ningún símbolo."
            while pila_operadores and precedencia[c] <= precedencia[pila_operadores[-1]]:
                salida.append(pila_operadores.pop())
            pila_operadores.append(c)
        else:
            # Carácter inválido
            return None

    while pila_operadores:
        if pila_operadores[-1] == '(' or pila_operadores[-1] == ')':
            # Paréntesis desequilibrados
            return None
        salida.append(pila_operadores.pop())

    return ''.join(salida)
