
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
#                       INICIA ANALIZADOR LEXICO
# -----------------------------------------------------------------------------
#palabras reservadas del lenguaje
reservadas = {
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
    x=caden.splitlines()
    filas=len(x)-1
    print("filas que no cambian: ",filas) 
    if h.filapivote>0:
        fila=(t.lineno-1)-h.filapivote*filas
    else:
        fila=(t.lineno-1)
    h.filapivote+=1
    print("Caracter lexico no permitido ==> '%s'" % t.value)
    h.errores+=  "<tr><td>"+str(t.value[0])+"</td><td>"+str(fila)+"</td><td>"+str(find_column(caden,t))+"</td><td>LEXICO</td><td>token no pertenece al lenguaje</td></tr>\n"
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



def p_inicio(t) :
    'inicio               : ETIQUETA DOSPUNTOS instrucciones inicio'
    #print(h.q)
    print("entra a inicio 1")
    if t[4]!=None:
        h.insertarSimbolos(t[4])
    p=[t[1],t[3]]

    if t[1]=="main":
        print("este si es main")
        h.insertarSimbolos(p)
        h.q.reverse()
        contador=0
        for i in h.q:
            if  i!=0:
                contador+=1
        print(contador)
        t[0]=h.q[0:contador]
    elif p!=None:
        h.insertarSimbolos(p)
    #para el reporte gramatical
    h.reporteGramatical1 +="INICIO     ->      MAIN DOSPUNTOS  bloque\n"
    h.reporteGramatical2 +="t[0] = t[1]\n"
    
    

def p_inicio_b(t) :
    'inicio               : ETIQUETA DOSPUNTOS instrucciones'
    print("entra a inicio 2")
    t[0]=[t[1],t[3]]
   
    print("+++++++ ",t[0])

def p_instrucciones_lista(t) :
    '''instrucciones    : instrucciones instruccion '''
    t[1].append(t[2])
    t[0]=t[1]
    h.reporteGramatical1 +="INSTRUCCIONES     ->      INSTRUCCIONES INSTRUCCION\n"
    h.reporteGramatical2 +="""t[1].append(t[2)]\n
    t[0] = t[1]\n"""


def p_instrucciones_instruccion(t) :
    'instrucciones    : instruccion '
    t[0]=[t[1]]
    h.reporteGramatical1 +="INSTRUCCIONES     ->      INSTRUCCION\n"
    h.reporteGramatical2 +="t[0] = [t[1]]\n"


def p_instruccion(t) :
    '''instruccion      : imprimir
                        | salto
                        | salida
                        | instruccion_if
                        | asignacion
                        | destruir'''
    t[0]=t[1]
    #print("salida ==> '%s'" % t[0])
    h.reporteGramatical1 +="INSTRUCCION     ->      Lista de instrucciones\n"
    h.reporteGramatical2 +="t[0] = t[1]\n"
   
def p_salida(t):
    'salida             : EXIT PUNTOYCOMA'
    t[0]=Salida(t[1])
    h.reporteGramatical1 +="EXIT    ->      EXIT PUNTOYCOMA\n"
    h.reporteGramatical2 +="t[0] = Salida(t[1])\n"

def p_salto(t):
    'salto             : GOTO ETIQUETA PUNTOYCOMA'
    t[0]=Goto(t[2])
    h.reporteGramatical1 +="SALTO    ->      GOTO ETIQUETA PUNTOYCOMA\n"
    h.reporteGramatical2 +="t[0] = \n"

def p_destruir(t):
    'destruir          : UNSET PARIZQUIERDO ID PARDERECHO'
    h.reporteGramatical1 +="DESTRUIR   ->      UNSET PARIZQUIERDO ID PARDERECHO\n"
    h.reporteGramatical2 +="t[0] = \n"

def p_imprimir_instruccion(t) :
    'imprimir     : PRINT PARIZQUIERDO final PARDERECHO PUNTOYCOMA'
    t[0]=Imprimir(t[3])
    h.reporteGramatical1 +="EXIT    ->      EXIT PUNTOYCOMA\n"
    h.reporteGramatical2 +="t[0] = Imprimir(t[3])\n"

def p_instruccion_if(t):
    'instruccion_if     : IF PARIZQUIERDO relacional PARDERECHO GOTO ETIQUETA PUNTOYCOMA'
    t[0]=If(t[3],t[6])
    h.reporteGramatical1 +="INSTRUCCION_IF    ->      IF PARIZQUIERDO RELACIONAL PARDERECHO GOTO ETIQUETA PUNTOYCOMA\n"
    h.reporteGramatical2 +="t[0] =  If(t[3],t[6])\n"

def p_asignacion(t):
    'asignacion         : ID IGUAL operacion PUNTOYCOMA'
    t[0]=Asignacion(t[1],t[3])
    h.reporteGramatical1 +="ASIGNACION    ->      ID IGUAL OPERACION PUNTOYCOMA\n"
    h.reporteGramatical2 +="t[0] = Asignacion(t[1],t[3])\n"


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
    h.reporteGramatical1 +="OPERACION    ->      UNA OPERACION\n"
    h.reporteGramatical2 +="t[0] = t[1]\n"

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
                    
def p_aritmetica(t):
    '''aritmetica         : final MAS final
                          | final MENOS final
                          | final POR final
                          | final DIV final
                          | final RESIDUO final'''
    if t[2]=='+': 
        t[0]=ExpresionAritmetica(t[1],t[3],OPERACION_ARITMETICA.MAS)
        h.reporteGramatical1 +="ARITMETICA    ->      FINAL + FINAL\n"
        h.reporteGramatical2 +="t[0]=ExpresionAritmetica(t[1],t[3],OPERACION_ARITMETICA.MAS)\n"
    elif t[2]=='-': 
        t[0]=ExpresionAritmetica(t[1],t[3],OPERACION_ARITMETICA.MENOS)
        h.reporteGramatical1 +="ARITMETICA    ->      FINAL - FINAL\n"
        h.reporteGramatical2 +="t[0]=ExpresionAritmetica(t[1],t[3],OPERACION_ARITMETICA.MENOS)\n"
    elif t[2]=='*': 
        t[0]=ExpresionAritmetica(t[1],t[3],OPERACION_ARITMETICA.POR)
        h.reporteGramatical1 +="ARITMETICA    ->      FINAL * FINAL\n"
        h.reporteGramatical2 +="t[0]=ExpresionAritmetica(t[1],t[3],OPERACION_ARITMETICA.POR)\n"
    elif t[2]=='/': 
        t[0]=ExpresionAritmetica(t[1],t[3],OPERACION_ARITMETICA.DIVIDIDO)
        h.reporteGramatical1 +="ARITMETICA    ->      FINAL / FINAL\n"
        h.reporteGramatical2 +="t[0]=ExpresionAritmetica(t[1],t[3],OPERACION_ARITMETICA.DIVIDIDO)\n"
    elif t[2]=='%': 
        t[0]=ExpresionAritmetica(t[1],t[3],OPERACION_ARITMETICA.RESIDUO)
        h.reporteGramatical1 +="ARITMETICA    ->      FINAL  FINAL\n"
        h.reporteGramatical2 +="t[0]=ExpresionAritmetica(t[1],t[3],OPERACION_ARITMETICA.RESIDUO)\n"

def p_aritmetica_abs(t):
    'aritmetica           : ABS PARIZQUIERDO final PARDERECHO'
    t[0]=ExpresionAbsoluto(t[3])
    h.reporteGramatical1 +="ARITMETICA    ->      ABS PARIZQUIERDO FINAL PARDERECHO\n"
    h.reporteGramatical2 +="t[0]=ExpresionAbsoluto(t[3])\n"


def p_logica(t):
    '''logica             : final AND final
                          | final OR final
                          | final XOR final'''
    if t[2]=='&&': 
        t[0]=ExpresionLogica(t[1],t[3],OPERACION_LOGICA.AND)
        h.reporteGramatical1 +="LOGICA    ->      FINAL AND FINAL\n"
        h.reporteGramatical2 +="t[0]=ExpresionLogica(t[1],t[3],OPERACION_LOGICA.AND)\n"
    elif t[2]=='||':
        t[0]=ExpresionLogica(t[1],t[3],OPERACION_LOGICA.OR)
        h.reporteGramatical1 +="LOGICA    ->      FINAL OR FINAL\n"
        h.reporteGramatical2 +="t[0]=ExpresionLogica(t[1],t[3],OPERACION_LOGICA.OR)\n"
    elif t[2]=='xor': 
        t[0]=ExpresionLogica(t[1],t[3],OPERACION_LOGICA.XOR)
        h.reporteGramatical1 +="LOGICA    ->      FINAL XOR FINAL\n"
        h.reporteGramatical2 +="t[0]=ExpresionLogica(t[1],t[3],OPERACION_LOGICA.XOR)\n"

def p_logica_not(t):
    'logica               : NOT final'
    t[0]=ExpresionLogicaNot(t[2])
    h.reporteGramatical1 +="LOGICA    ->      NOT FINAL\n"
    h.reporteGramatical2 +="t[0]=ExpresionLogicaNot(t[2])\n"

def p_bit(t):
    '''bit                : final AND2 final
                          | final OR2 final
                          | final XOR2 final
                          | final DESPLAZAMIENTOIZQ final
                          | final DESPLAZAMIENTODER final'''
    if t[2]=='&': 
        t[0]=ExpresionBit(t[1],t[3],OPERACION_BIT.AND)
        h.reporteGramatical1 +="BIT    ->      FINAL AND2 FINAL\n"
        h.reporteGramatical2 +="t[0]=ExpresionBit(t[1],t[3],OPERACION_BIT.AND)\n"
    elif t[2]=='|': 
        t[0]=ExpresionBit(t[1],t[3],OPERACION_BIT.OR)
        h.reporteGramatical1 +="BIT    ->      FINAL OR2 FINAL\n"
        h.reporteGramatical2 +="t[0]=ExpresionBit(t[1],t[3],OPERACION_BIT.OR)\n"
    elif t[2]=='^': 
        t[0]=ExpresionBit(t[1],t[3],OPERACION_BIT.XOR)
        h.reporteGramatical1 +="BIT    ->      FINAL XOR2 FINAL\n"
        h.reporteGramatical2 +="t[0]=ExpresionBit(t[1],t[3],OPERACION_BIT.XOR)\n"
    elif t[2]=='<<': 
        t[0]=ExpresionBit(t[1],t[3],OPERACION_BIT.DESPLAZAMIENTO_IZQUIERDA)
        h.reporteGramatical1 +="BIT    ->      FINAL DESPLAZAMIENTOIZQ FINAL\n"
        h.reporteGramatical2 +="t[0]=ExpresionBit(t[1],t[3],OPERACION_BIT.DESPLAZAMIENTO_IZQUIERDA)\n"
    elif t[2]=='>>': 
        t[0]=ExpresionBit(t[1],t[3],OPERACION_BIT.DESPLAZAMIENTO_DERECHA)
        h.reporteGramatical1 +="BIT    ->      FINAL DESPLAZAMIENTODER FINAL\n"
        h.reporteGramatical2 +="t[0]=ExpresionBit(t[1],t[3],OPERACION_BIT.DESPLAZAMIENTO_DERECHA)\n"

def p_bit_not(t):
    'bit                  : NOT2 final'
    t[0]=ExpresionBitNot(t[2])
    h.reporteGramatical1 +="BIT    ->      NOT2 FINAL\n"
    h.reporteGramatical2 +="t[0]=ExpresionBitNot(t[2])\n"

def p_relacional(t):
    '''relacional         : final IGUALIGUAL final
                          | final DIFERENTE final
                          | final MAYORIGUAL final
                          | final MENORIGUAL final
                          | final MAYOR final
                          | final MENOR final'''
    if t[2]=='==': 
        t[0]=ExpresionRelacional(t[1],t[3],OPERACION_RELACIONAL.IGUAL_IGUAL)
        h.reporteGramatical1 +="RELACIONAL    ->      FINAL IGUALIGUAL FINAL\n"
        h.reporteGramatical2 +="t[0]=ExpresionRelacional(t[1],t[3],OPERACION_RELACIONAL.IGUAL_IGUAL)\n"
    elif t[2]=='!=': 
        t[0]=ExpresionRelacional(t[1],t[3],OPERACION_RELACIONAL.NO_IGUAL)
        h.reporteGramatical1 +="RELACIONAL    ->      FINAL DIFERENTE FINAL\n"
        h.reporteGramatical2 +="t[0]=ExpresionRelacional(t[1],t[3],OPERACION_RELACIONAL.NO_IGUAL)\n"
    elif t[2]=='>=': 
        t[0]=ExpresionRelacional(t[1],t[3],OPERACION_RELACIONAL.MAYOR_IGUAL)
        h.reporteGramatical1 +="RELACIONAL    ->      FINAL MAYORIGUAL FINAL\n"
        h.reporteGramatical2 +="t[0]=ExpresionRelacional(t[1],t[3],OPERACION_RELACIONAL.MAYOR_IGUAL)\n"
    elif t[2]=='<=': 
        t[0]=ExpresionRelacional(t[1],t[3],OPERACION_RELACIONAL.MENOR_IGUAL)
        h.reporteGramatical1 +="RELACIONAL    ->      FINAL MENORIGUAL FINAL\n"
        h.reporteGramatical2 +="t[0]=ExpresionRelacional(t[1],t[3],OPERACION_RELACIONAL.MENOR_IGUAL)\n"
    elif t[2]=='>': 
        t[0]=ExpresionRelacional(t[1],t[3],OPERACION_RELACIONAL.MAYOR)
        h.reporteGramatical1 +="RELACIONAL    ->      FINAL MAYOR FINAL\n"
        h.reporteGramatical2 +="t[0]=ExpresionRelacional(t[1],t[3],OPERACION_RELACIONAL.MAYOR)\n"
    elif t[2]=='<': 
        t[0]=ExpresionRelacional(t[1],t[3],OPERACION_RELACIONAL.MENOR)
        h.reporteGramatical1 +="RELACIONAL    ->      FINAL MENOR FINAL\n"
        h.reporteGramatical2 +="t[0]=ExpresionRelacional(t[1],t[3],OPERACION_RELACIONAL.MENOR)\n"

def p_final(t):
    '''final              : DECIMAL
                          | ENTERO'''
    t[0]=ExpresionNumero(t[1])
    h.reporteGramatical1 +="FINAL    ->      ID("+str(t[1])+")\n"
    h.reporteGramatical2 +="t[0]=ExpresionNumero(t[1])\n"

def p_final_id(t):
    'final              : ID'
    t[0]=ExpresionIdentificador(t[1])
    h.reporteGramatical1 +="FINAL    ->      ID("+str(t[1])+")\n"
    h.reporteGramatical2 +="t[0]=ExpresionIdentificador(t[1])\n"

def p_artimetica_negativo(t):
    'final : MENOS final %prec UMENOS'
    t[0]=ExpresionNegativo(t[2])
    h.reporteGramatical1 +="FINAL    ->      MENOS FINAL\n"
    h.reporteGramatical2 +="t[0]=ExpresionNegativo(t[2])\n"

import ventana as k
from PyQt5 import QtCore, QtGui, QtWidgets
def takeinputs(a): 
    name, done1 = QtWidgets.QInputDialog.getText( 
        a.ventanaCentrada, 'Input Dialog', 'Enter your name:') 
    if done1: 
        print(name)
        return name
    return "j"

def p_final_read(t):
    'final              : READ PARIZQUIERDO PARDERECHO'
    x = input('ingrese un valor: ')
    t[0]=ExpresionSimpleComilla(x)
    h.reporteGramatical1 +="FINAL    ->      READ PARIZQUIERDO PARDERECHO\n"
    h.reporteGramatical2 +="x = input('ingrese un valor: ') \nt[0]=ExpresionSimpleComilla(x)\n"

def p_final_array(t):
    'final              : ARRAY PARIZQUIERDO PARDERECHO'  
    h.reporteGramatical1 +="FINAL    ->      "+t[1]+"\n"
    h.reporteGramatical2 +="\n"  

def p_final_cadena(t):
    'final              : CADENA'
    t[0]=ExpresionSimpleComilla(t[1])
    h.reporteGramatical1 +="FINAL    ->      CADENA ("+t[1]+")\n"
    h.reporteGramatical2 +="t[0]=ExpresionSimpleComilla(t[1])\n"


#para manejar los errores sintacticos
#def p_error(t): #en modo panico :v
  #  print("token error: ",t)
   # print("Error sintáctico en '%s'" % t.value[0])
   # print("Error sintáctico en '%s'" % t.value[1])
    

#def p_error(t): #en modo panico :v
#   while True:
#        tok=parser.token()
#        if not tok or tok.type==';':break
#    parser.errok()
#    return tok
def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    #print((token.lexpos - line_start) +1 )
    return (token.lexpos - line_start) 


def p_error(t):
     print("token: '%s'" %t)
     print("Error sintáctico en '%s' " % t.value)
     #h.filapivote+=1
     x=caden.splitlines()
     filas=len(x)-1
     print("filas que no cambian: ",filas)
     
     if h.filapivote>0:
         fila=(t.lineno-1)-h.filapivote*filas
     else:
         fila=(t.lineno-1)
     h.filapivote+=1
     h.errores+=  "<tr><td>"+str(t.value)+"</td><td>"+str(fila)+"</td><td>"+str(find_column(caden,t))+"</td><td>SINTACTICO</td><td>el token no va aqui</td></tr>\n"
     print("Error sintáctico fila '%s'" % fila)
     print("Error sintáctico col '%s'" % find_column(caden,t))
     if not t:
         print("End of File!")
         return
     # Read ahead looking for a closing '}'
     while True:
         tok = parser.token()             # Get the next token
         if not tok or tok.type == 'PUNTOYCOMA': 
             break
     parser.restart()
     





import ply.yacc as yacc
parser = yacc.yacc()

def parse(input) :
    h.q=[0]*100
    global caden
    caden=""
    caden=input
    return parser.parse(input)