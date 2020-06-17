class Instruccion:
    '''This is an abstract class'''

class Imprimir(Instruccion) :
    '''
        Esta clase representa la instrucción imprimir.
        La instrucción imprimir únicamente tiene como parámetro una cadena
    '''

    def __init__(self,  cad) :
        self.cad = cad


class Definicion(Instruccion) :
    '''
        Esta clase representa la instrucción de definición de variables.
        Recibe como parámetro el nombre del identificador a definir
    '''

    def __init__(self, id) :
        self.id = id
        
class Asignacion(Instruccion) :
    '''
        Esta clase representa la instrucción de asignación de variables
        Recibe como parámetro el identificador a asignar y el valor que será asignado.
    '''

    def __init__(self, id, expNumerica) :
        self.id = id
        self.expNumerica = expNumerica


class If(Instruccion) : #es la que se l lamaba ifElse
    '''
        Esta clase representa la instrucción if-else.
        La instrucción if-else recibe como parámetro una expresión lógica y la lista
        de instrucciones a ejecutar si la expresión lógica es verdadera y otro lista de instrucciones
        a ejecutar si la expresión lógica es falsa.
    '''

    def __init__(self, expLogica, instrIfFalso = []) :
        self.expLogica = expLogica
        self.instrIfFalso = instrIfFalso

class Salida(Instruccion):
    '''
        Esta clase representa la exit
        La instrucción unicamente el parametro exit jaja
    '''    
    def __init__(self, id) :
        self.id = id

class Etiquetas(Instruccion) :
    '''
        Esta clase representa un bloque de instrucciones con su tag
        Recibe como parámetro la etiqueta del bloque y sus sentencias o instruciones y eso
    '''

    def __init__(self, id, sentencias) :
        self.id = id
        self.sentencias = sentencias

class Goto(Instruccion) :
    '''
        Esta clase representa un bloque de instrucciones con su tag
        Recibe como parámetro la etiqueta del bloque y sus sentencias o instruciones y eso
    '''

    def __init__(self, etiqueta) :
        self.etiqueta = etiqueta


