# Jerarquia de los operadores
precedence = {'*': 3, '+': 2, '.': 1}

def infix_to_postfix(infix):
    # Pila y  lista de salida vacías
    stack = []
    output = []
    # listado de tokens
    tokens = list(infix)
    
    # Proceso para validar la expresión regular
    left_paren_count = tokens.count('(')
    right_paren_count = tokens.count(')')
    if left_paren_count != right_paren_count:
        raise ValueError('Error en la expresión regular de entrada. Paréntesis desbalanceados.')
    
    prev_token = None
    for token in tokens:
        if token.isalpha() or token.isdigit():
            # Si el token es un carácter o un dígito, agregarlo a la lista de salida
            output.append(token)
        elif token in '*+.':
            # Si el token es un operador, sacar los operadores de mayor o igual precedencia de la pila y agregarlos a la lista de salida
            if prev_token is None or prev_token in '*+.' or prev_token == '(':
                raise ValueError('La expresión regular ingresada es incorrecta. El operador {} no se está aplicando a ningún símbolo.'.format(token))
            while stack and stack[-1] != '(' and precedence[token] <= precedence.get(stack[-1], 0):
                output.append(stack.pop())
            # Agregar el operador a la pila
            stack.append(token)
        elif token == '(':
            # Si el token es un paréntesis izquierdo, agregarlo a la pila
            if prev_token is not None and prev_token not in '*+.' and prev_token != '(':
                raise ValueError('La expresión regular ingresada es incorrecta. El paréntesis izquierdo no está precedido por un operador.')
            stack.append(token)
        elif token == ')':
            # Si el token es un paréntesis derecho, sacar los operadores de la pila y agregarlos a la lista de salida hasta que se encuentre el paréntesis izquierdo correspondiente
            if prev_token is None or prev_token in '*+.' or prev_token == '(':
                raise ValueError('La expresión regular ingresada es incorrecta. El paréntesis derecho no está precedido por un símbolo o un paréntesis izquierdo.')
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            # Sacar el paréntesis izquierdo de la pila
            stack.pop()
        
        prev_token = token

    # Sacar los operadores restantes de la pila y agregarlos a la lista de salida
    while stack:
        output.append(stack.pop())

    # Convertir la lista de salida en una cadena y devolverla
    return ''.join(output)