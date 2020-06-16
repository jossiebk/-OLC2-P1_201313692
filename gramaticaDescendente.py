# -----------------------------------------------------------------------------
# Jossie Bismarck Castrillo Fajardo
# 201313692
#
# Universidad de San Carlos de Guatemala
# Facultad de Ingenieria
# Escuela de Ciencias y Sistemas
# Organizacion de Lenguajes y Compiladores 2
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
#                       INICIA ANALIZADOR LEXICO DESCENDENTE
# -----------------------------------------------------------------------------
#palabras reservadas del lenguaje
reservadas = {
    'main' : 'MAIN',
    'goto' : 'GOTO',
    'unset' : 'UNSET',
    'print' : 'PRINT',
    'exit' : 'EXIT',
    'int' : 'INT',
    'float' : 'FLOAT',
    'char' : 'CHAR',
    'abs' : 'ABS',
    'if' : 'IF',
    'read' : 'READ',
    'array' : 'ARRAY',
    'xor':'XOR'
}
# listado de tokens que manejara el lenguaje (solo la forma en la que los llamare  en las producciones)
tokens  = [
    'PUNTOYCOMA',
    'DOSPUNTOS',
    'PARIZQUIERDO',
    'PARDERECHO',
    'IGUAL',
    'MAS',
    'MENOS',
    'POR',
    'DIV',
    'RESIDUO',
    'NOT',
    'AND',
    'OR',
    'NOT2',
    'AND2',
    'OR2',
    'XOR2',
    'DESPLAZAMIENTOIZQ',
    'DESPLAZAMIENTODER',
    'IGUALIGUAL',
    'DIFERENTE',
    'MAYORIGUAL',
    'MENORIGUAL',
    'MAYOR',
    'MENOR',
    'CORCHETEDER',
    'CORCHETEIZQ',
    'DECIMAL',
    'ENTERO',
    'CADENA',
    'ETIQUETA',
    'ID'
] + list(reservadas.values())

# Tokens y la forma en la que se usaran en el lenguaje
t_PUNTOYCOMA        = r';'
t_DOSPUNTOS         = r':'
t_PARIZQUIERDO      = r'\('
t_PARDERECHO        = r'\)'
t_IGUAL             = r'='
t_MAS               = r'\+'
t_MENOS             = r'-'
t_POR               = r'\*'
t_DIV               = r'/'
t_RESIDUO           = r'%'
t_NOT               = r'!'
t_AND               = r'&&'
t_OR                = r'\|\|'
t_XOR               = r'xor'
t_NOT2              = r'~'
t_AND2              = r'&'
t_OR2               = r'\|'
t_XOR2              = r'\^'
t_DESPLAZAMIENTOIZQ = r'<<'
t_DESPLAZAMIENTODER = r'>>'
t_IGUALIGUAL        = r'=='
t_DIFERENTE         = r'!='
t_MAYORIGUAL        = r'>='
t_MENORIGUAL        = r'<='
t_MAYOR             = r'>'
t_MENOR             = r'<'
t_CORCHETEDER = r']'
t_CORCHETEIZQ = r'\['

#definife la estructura de los decimales
def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("El valor decimal es muy largo %d", t.value)
        t.value = 0
    return t
#definife la estructura de los enteros
def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("El valor del entero es muy grande %d", t.value)
        t.value = 0
    return t
#definife la estructura de los identificadores que en este caso seran $letra y numero
def t_ID(t):
     r'\$[t|a|v|ra|s|p]+[0-9]*'
     t.type = reservadas.get(t.value.lower(),'ID')    # Check for reserved words
     return t
#definife la estructura de las cadenas
def t_CADENA(t):
    r'\'.*?\''
    t.value = t.value[1:-1] # quito las comillas del inicio y final de la cadena
    return t 
#definife la estructura de las etiquetas, por el momento las tomo unicamente como letras y numeros
def t_ETIQUETA(t):
     r'[a-zA-Z0-9]+'
     t.type = reservadas.get(t.value.lower(),'ETIQUETA')    # Check for reserved words
     return t

# Comentario simple # ...
def t_COMENTARIO_SIMPLE(t):
    r'\#.*\n'
    t.lexer.lineno += 1

# ----------------------- Caracteres ignorados -----------------------
# caracter equivalente a un tab
t_ignore = " \t"
#caracter equivalente a salto de linea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Caracter lexico no permitido ==> '%s'" % t.value[0])
    t.lexer.skip(1)

# Construyendo el analizador léxico
import ply.lex as lex
lexer = lex.lex()


# -----------------------------------------------------------------------------
#                       INICIA ANALIZADOR SINTACTICO
# -----------------------------------------------------------------------------

# Asociación de operadores y precedencia
precedence = (
    ('left','NOT','NOT2'),
    ('left','MAS','MENOS'),
    ('left','POR','DIV'),
    ('left','AND','OR','RESIDUO','XOR'),
    ('left','AND2','OR2','DESPLAZAMIENTOIZQ','XOR2','DESPLAZAMIENTODER'),
    ('left','IGUALIGUAL','DIFERENTE','MAYORIGUAL','MENORIGUAL','MAYOR','MENOR'),
    ('right','UMENOS'),
    )

# estructura de mi gramatica
import reportes as h
from expresiones import *
from instrucciones import *

# estructura de mi gramatica

def p_inicio(t) :
    'inicio               : MAIN DOSPUNTOS bloque'
    t[0]=t[3]


def p_bloque_lista(t):
    '''bloque             : bloque ETIQUETA DOSPUNTOS instrucciones
                          | bloque instrucciones'''
    if t[3]==':': 
        t[1].append(t[4])
        t[0]=t[1]
    else:
        t[1].append(t[2])
        t[0]=t[1]     
 
def p_bloque(t):
    'bloque             : ETIQUETA DOSPUNTOS instrucciones'
    t[0]=t[3]

def p_bloque2(t):
    'bloque             : instrucciones'
    t[0]=t[1]

def p_instrucciones_lista(t) :
    '''instrucciones    : instrucciones instruccion '''
    t[1].append(t[2])
    t[0]=t[1]

def p_instrucciones_instruccion(t) :
    'instrucciones    : instruccion '
    t[0]=[t[1]]

def p_instruccion(t) :
    '''instruccion      : imprimir
                        | salto
                        | salida
                        | instruccion_if
                        | asignacion
                        | destruir'''
    t[0]=t[1]
   
def p_salida(t):
    'salida             : EXIT PUNTOYCOMA'
    t[0]=Salida(t[1])

def p_salto(t):
    'salto             : GOTO ETIQUETA PUNTOYCOMA'

def p_destruir(t):
    'destruir          : UNSET PARIZQUIERDO ID PARDERECHO'

def p_imprimir_instruccion(t) :
    'imprimir     : PRINT PARIZQUIERDO final PARDERECHO PUNTOYCOMA'
    t[0]=Imprimir(t[3])

def p_instruccion_if(t):
    'instruccion_if     : IF PARIZQUIERDO relacional PARDERECHO GOTO ETIQUETA PUNTOYCOMA'
    t[0]=If(t[3],t[6])

def p_asignacion(t):
    'asignacion         : ID IGUAL operacion PUNTOYCOMA'
    t[0]=Asignacion(t[1],t[3])

# empiezan las producciones de las operaciones finales
#la englobacion de las operaciones
def p_operacion(t):
    '''operacion        : conversion
                        | aritmetica
                        | logica
                        | bit
                        | relacional
                        | final'''
    t[0]=t[1]
def p_conversion(t):
    '''conversion         : PARIZQUIERDO INT PARDERECHO final
                          | PARIZQUIERDO FLOAT PARDERECHO final
                          | PARIZQUIERDO CHAR PARDERECHO final'''
    if t[2]=='int': 
        t[0]=ExpresionCasteo(t[4],OPERACION_CASTEO.ENTERO)
        h.reporteGramatical1 +="CONVERSION    ->      PARIZQUIERDO INT PARDERECHO FINAL\n"
        h.reporteGramatical2 +="t[0]=ExpresionCasteo(t[4],OPERACION_CASTEO.ENTERO)\n"
    elif t[2]=='float': 
        t[0]=ExpresionCasteo(t[4],OPERACION_CASTEO.FLOTANTE)
        h.reporteGramatical1 +="CONVERSION    ->      PARIZQUIERDO FLOAT PARDERECHO FINAL\n"
        h.reporteGramatical2 +="t[0]=ExpresionCasteo(t[4],OPERACION_CASTEO.FLOTANTE)\n"
    elif t[2]=='char': 
        t[0]=ExpresionCasteo(t[4],OPERACION_CASTEO.CARACTER)
        h.reporteGramatical1 +="CONVERSION    ->      PARIZQUIERDO CHAR PARDERECHO FINAL\n"
        h.reporteGramatical2 +="t[0]=ExpresionCasteo(t[4],OPERACION_CASTEO.CARACTER)\n"


 #--------------------------------------------------------aca voy----------------------------------------------------------      
def p_aritmetica(t):
    'aritmetica          : final aritmetica_prima'
    a=t[2]
    b=a[0]
    c=a[1]
    t[0]=ExpresionAritmetica(t[1],b,c)

def p_aritmetica_prima(t):
    '''aritmetica_prima         : MAS final
                                | MENOS final
                                | POR final
                                | DIV final
                                | RESIDUO final'''
    if t[1]=='+': 
        t[0]=[t[2],OPERACION_ARITMETICA.MAS]
    elif t[1]=='-': 
        t[0]=[t[2],OPERACION_ARITMETICA.MENOS]
    elif t[1]=='*': 
        t[0]=[t[2],OPERACION_ARITMETICA.POR]
    elif t[1]=='/': 
        t[0]=[t[2],OPERACION_ARITMETICA.DIVIDIDO]
    elif t[1]=='%': 
        t[0]=[t[2],OPERACION_ARITMETICA.RESIDUO]

def p_aritmetica_abs(t):
    'aritmetica           : ABS PARIZQUIERDO final PARDERECHO'
    t[0]=ExpresionAbsoluto(t[3])

def p_logica(t):
     'logica          : final logica_prima'
     a=t[2]
     b=a[0]
     c=a[1]
     t[0]=ExpresionLogica(t[1],b,c)

def p_logica_prima(t):
    '''logica_prima             : AND final
                                | OR final
                                | XOR final'''
    if t[1]=='&&': 
        t[0]=[t[2],OPERACION_LOGICA.AND]
    elif t[1]=='||':
        t[0]=[t[2],OPERACION_LOGICA.OR]
    elif t[1]=='xor': 
        t[0]=[t[2],OPERACION_LOGICA.XOR]
                            
def p_logica_not(t):
    'logica               : NOT final'
    t[0]=ExpresionLogicaNot(t[2])

def p_bit(t):
     'bit          : final bit_prima'
     a=t[2]
     b=a[0]
     c=a[1]
     t[0]=ExpresionBit(t[1],b,c)

def p_bit_prima(t):
    '''bit_prima          : AND2 final
                          | OR2 final
                          | XOR2 final
                          | DESPLAZAMIENTOIZQ final
                          | DESPLAZAMIENTODER final'''
    if t[1]=='&': 
        t[0]=[t[2],OPERACION_BIT.AND]
    elif t[1]=='|': 
        t[0]=[t[2],OPERACION_BIT.OR]
    elif t[1]=='^': 
        t[0]=[t[2],OPERACION_BIT.XOR]
    elif t[1]=='<<': 
        t[0]=[t[2],OPERACION_BIT.DESPLAZAMIENTO_IZQUIERDA]
    elif t[1]=='>>': 
        t[0]=[t[2],OPERACION_BIT.DESPLAZAMIENTO_DERECHA]

def p_bit_not(t):
    'bit                  : NOT2 final'
    t[0]=ExpresionBitNot(t[2])

def p_relacional(t):
     'relacional          : final relacional_prima'
     a=t[2]
     b=a[0]
     c=a[1]
     t[0]=ExpresionRelacional(t[1],b,c)

def p_relacional_prima(t):
    '''relacional_prima         : IGUALIGUAL final
                                | DIFERENTE final
                                | MAYORIGUAL final
                                | MENORIGUAL final
                                | MAYOR final
                                | MENOR final'''
    if t[1]=='==': 
        t[0]=[t[2],OPERACION_RELACIONAL.IGUAL_IGUAL]
    elif t[1]=='!=': 
        t[0]=[t[2],OPERACION_RELACIONAL.IGUAL_IGUAL]
    elif t[1]=='>=': 
        t[0]=[t[2],OPERACION_RELACIONAL.IGUAL_IGUAL]
    elif t[1]=='<=': 
       t[0]=[t[2],OPERACION_RELACIONAL.IGUAL_IGUAL]
    elif t[1]=='>': 
        t[0]=[t[2],OPERACION_RELACIONAL.IGUAL_IGUAL]
    elif t[1]=='<': 
        t[0]=[t[2],OPERACION_RELACIONAL.IGUAL_IGUAL]


def p_final(t):
    '''final              : DECIMAL
                          | ENTERO'''
    t[0]=ExpresionNumero(t[1])

def p_final_id(t):
    'final              : ID'
    t[0]=ExpresionIdentificador(t[1])

def p_artimetica_negativo(t):
    'final : MENOS final %prec UMENOS'
    t[0]=ExpresionNegativo(t[2])

def p_final_read(t):
    'final              : READ PARIZQUIERDO PARDERECHO'
    x = input('ingrese un valor: ')
    t[0]=ExpresionSimpleComilla(x)

def p_final_array(t):
    'final              : ARRAY PARIZQUIERDO PARDERECHO'  


def p_final_cadena(t):
    'final              : CADENA'
    t[0]=ExpresionSimpleComilla(t[1])

def p_empty(t):
    'empty :'
    t[0]=t[-3]

#para manejar los errores sintacticos
def p_error(t): #en modo panico :v
    print("token error: ",t)
    print("Error sintáctico en '%s'" % t)




import ply.yacc as yacc
parser = yacc.yacc()

def parse(input) :
    return parser.parse(input)