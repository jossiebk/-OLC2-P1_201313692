from enum import Enum

class OPERACION_ARITMETICA(Enum) :
    MAS = 1
    MENOS = 2
    POR = 3
    DIVIDIDO = 4
    RESIDUO = 5
    ABSOLUTO = 6

class OPERACION_LOGICA(Enum) :
    NOT  = 1
    AND = 2
    OR = 3
    XOR = 4

class OPERACION_BIT(Enum):
    NOT = 1
    AND = 2
    OR = 3
    XOR= 4
    DESPLAZAMIENTO_IZQUIERDA = 5
    DESPLAZAMIENTO_DERECHA = 6

class OPERACION_RELACIONAL(Enum):
    IGUAL_IGUAL = 1
    NO_IGUAL = 2
    MAYOR_IGUAL = 3
    MENOR_IGUAL = 4
    MAYOR = 5
    MENOR = 6

class OPERACION_CASTEO(Enum):
    ENTERO = 1
    FLOTANTE = 2
    CARACTER = 3

class ExpresionNumerica:
    '''
        Esta clase representa una expresión numérica
    '''

class ExpresionAritmetica(ExpresionNumerica) :
    '''
        Esta clase representa la Expresión Aritmética.
        Esta clase recibe los operandos y el operador
    '''

    def __init__(self, exp1, exp2, operador) :
        self.exp1 = exp1
        self.exp2 = exp2
        self.operador = operador

class ExpresionNegativo(ExpresionNumerica) :
    '''
        Esta clase representa la Expresión Aritmética Negativa
        Esta clase recibe la expresion
    '''
    def __init__(self, exp) :
        self.exp = exp

class ExpresionAbsoluto(ExpresionNumerica) :
    '''
        Esta clase representa la Expresión Aritmética para obtener su valor absoluto.
        Esta clase recibe la expresion
    '''
    def __init__(self, exp) :
        self.exp = exp

class ExpresionNumero(ExpresionNumerica) :
    '''
        Esta clase representa una expresión numérica entera o decimal.
    '''

    def __init__(self, val = 0) :
        self.val = val

class ExpresionIdentificador(ExpresionNumerica) :
    '''
        Esta clase representa un identificador.
    '''

    def __init__(self, id = "") :
        self.id = id

class ExpresionRelacional(ExpresionNumerica):
    '''
        Esta clase representa la Expresión Relacional.
        Esta clase recibe los operandos y el operador
    '''

    def __init__(self, exp1, exp2, operador) :
        self.exp1 = exp1
        self.exp2 = exp2
        self.operador = operador

class ExpresionCadena :
    '''
        Esta clase representa una Expresión de tipo cadena.
    '''


class ExpresionSimpleComilla(ExpresionCadena) :
    '''
        Esta clase representa una cadena entre comillas simples.
        Recibe como parámetro el valor del token procesado por el analizador léxico
    '''

    def __init__(self, val) :
        self.val = val


class ExpresionLogica(ExpresionNumerica) :
    '''
        Esta clase representa la expresión lógica.
        Esta clase recibe los operandos y el operador
    '''

    def __init__(self, exp1, exp2, operador) :
        self.exp1 = exp1
        self.exp2 = exp2
        self.operador = operador

class ExpresionLogicaNot(ExpresionNumerica):
    '''
        Esta clase representa la expresión lógica para el not.
        Esta clase recibe un operando y el operador !
    '''
    def __init__(self, exp) :
        self.exp = exp


class ExpresionBit(ExpresionNumerica) :
    '''
        Esta clase representa la expresión bit a bit.
        Esta clase recibe los operandos y el operador
    '''

    def __init__(self, exp1, exp2, operador) :
        self.exp1 = exp1
        self.exp2 = exp2
        self.operador = operador

class ExpresionBitNot(ExpresionNumerica):
    '''
        Esta clase representa la expresión bit a bit para el not.
        Esta clase recibe un operando y el operador ~ o este colocho
    '''
    def __init__(self, exp) :
        self.exp = exp


class ExpresionCasteo(ExpresionNumerica):
    '''
        Esta clase representa la expresión para castear datos.
        Esta clase recibe un tipo a convertir y el dato
    '''
    def __init__(self, exp, operador) :
        self.exp = exp
        self.operador = operador #este sera el tipo a convertir