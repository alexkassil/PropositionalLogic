import string

from buffer import Buffer



SYMBOL = set(string.ascii_lowercase + string.ascii_uppercase + string.digits + '_')
WHITESPACE = set(' \t\n\r')
DELIMITERS = set('(,)')

circuits = {
    'c_nand' : 'NAND GATE : 2 Inputs\nReturns not(a and b)'
}

master_circuits = {
    'c_not'  : 'NOT GATE : 1 Input\nReturns c_nand(a, a)',
    'c_and'  : 'AND GATE : 2 Inputs\nReturns c_not(c_nand(a, b))',
    'c_or'   : 'OR GATE : 2 Inputs\nReturns c_nand(c_nand(a, a), c_nand(b, b))',
    'c_xor'  : 'XOR GATE : 2 Inputs\nReturns c_and(c_or(a, b), c_nand(a, b))',
    'c_nor'  : 'NOR GATE : 2 Inputs\nReturns c_not(c_or(a, b))',
    'c_and_8': 'AND GATE : 8 Inputs\nReturns c_and(c_and(c_and(a, b), c_and(c, d)), c_and(c_and(e, f), c_and(g, h)))'
}

def tokenize(s):
    src = Buffer(s)
    tokens = []
    while True:
        token = next_token(src)
        if token is None:
            return tokens
        tokens.append(token)

def take(src, allowed_characters):
    result = ''
    while src.current() in allowed_characters:
        result += src.remove_front()
    return result

def next_token(src):
    take(src, WHITESPACE)
    c = src.current()
    if c is None:
        return None
    elif c in SYMBOL:
        return take(src, SYMBOL)
    elif c in DELIMITERS:
        src.remove_front()
        return c
    else:
        raise SyntaxError("'{}' is not a token".format(c))

def is_input(token):
    for char in token:
        if char not in SYMBOL:
            return False
    return True
    
def find_inputs(tokens):
    inputs = []
    for token in tokens:
        if is_input(token) and token not in circuits and token not in inputs:
            inputs.append(token)
    return inputs

