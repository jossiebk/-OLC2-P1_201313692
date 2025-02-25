import gramaticaDescendente as g
import re
import tablaDeSimbolos as TS
from expresiones import *
from instrucciones import *
import reportes as h

def procesar_imprimir(instr, ts) :
    cadena=resolver_cadena(instr.cad, ts)
    if cadena.count('\\n')>0:
        print('Jossie>', resolver_cadena(instr.cad, ts).replace("\\n","\nJossie>"))
    else:
        print('Jossie>', resolver_cadena(instr.cad, ts))

def procesar_asignacion(instr, ts) :  
    if ver_tipo_expresion(instr.expNumerica,ts)==1:
        simbolo = TS.Simbolo(instr.id, TS.TIPO_DE_DATO.NUMERO, 0)      # inicializamos con 0 como valor por defecto
        ts.agregar(simbolo)
        val = resolver_expresion_aritmetica(instr.expNumerica, ts)
        simbolo = TS.Simbolo(instr.id, TS.TIPO_DE_DATO.NUMERO, val)
        ts.actualizar(simbolo)
    elif ver_tipo_expresion(instr.expNumerica,ts)==2:
        simbolo = TS.Simbolo(instr.id, TS.TIPO_DE_DATO.NUMERO, 0)      # inicializamos con 0 como valor por defecto
        ts.agregar(simbolo)
        val = resolver_expresion_logica(instr.expNumerica, ts)
        simbolo = TS.Simbolo(instr.id, TS.TIPO_DE_DATO.NUMERO, val)
        ts.actualizar(simbolo)
    elif ver_tipo_expresion(instr.expNumerica,ts)==3:
        simbolo = TS.Simbolo(instr.id, TS.TIPO_DE_DATO.NUMERO, 0)      # inicializamos con 0 como valor por defecto
        ts.agregar(simbolo)
        val = resolver_expresion_bit(instr.expNumerica, ts)
        simbolo = TS.Simbolo(instr.id, TS.TIPO_DE_DATO.NUMERO, val)
        ts.actualizar(simbolo)
    elif ver_tipo_expresion(instr.expNumerica,ts)==4:
        simbolo = TS.Simbolo(instr.id, TS.TIPO_DE_DATO.NUMERO, 0)      # inicializamos con 0 como valor por defecto
        ts.agregar(simbolo)
        val = resolver_expresion_relacional(instr.expNumerica, ts)
        simbolo = TS.Simbolo(instr.id, TS.TIPO_DE_DATO.NUMERO, val)
        ts.actualizar(simbolo)
    elif ver_tipo_expresion(instr.expNumerica,ts)==5:
        val = resolver_expresion_aritmetica(instr.expNumerica, ts)
        simbolo = TS.Simbolo(instr.id, TS.TIPO_DE_DATO.NUMERO, val)
        ts.agregar(simbolo)
    elif ver_tipo_expresion(instr.expNumerica,ts)==6:      # inicializamos con el valor que venga
        val = resolver_expresion_aritmetica(instr.expNumerica, ts)
        simbolo = TS.Simbolo(instr.id, TS.TIPO_DE_DATO.NUMERO, val)
        ts.agregar(simbolo)
    elif ver_tipo_expresion(instr.expNumerica,ts)==7:
        simbolo = TS.Simbolo(instr.id, TS.TIPO_DE_DATO.NUMERO, 0)      # inicializamos con 0 como valor por defecto
        ts.agregar(simbolo)
        val = resolver_casteo(instr.expNumerica, ts)
        simbolo = TS.Simbolo(instr.id, TS.TIPO_DE_DATO.NUMERO, val)
        ts.actualizar(simbolo)
    

def ver_tipo_expresion(exp,ts):
     if isinstance(exp, ExpresionAritmetica) : return 1
     elif isinstance(exp,ExpresionLogica): return 2
     elif isinstance(exp,ExpresionBit): return 3
     elif isinstance(exp,ExpresionRelacional): return 4
     elif isinstance(exp,ExpresionLogicaNot): return 2
     elif isinstance(exp,ExpresionBitNot): return 3
     elif isinstance(exp,ExpresionNumero): return 5
     elif isinstance(exp,ExpresionNegativo): return 5
     elif isinstance(exp,ExpresionSimpleComilla): return 6
     elif isinstance(exp,ExpresionAbsoluto): return 5
     elif isinstance(exp,ExpresionCasteo): return 7

    

def procesar_if(instr, ts) :
    val = resolver_expresion_logica(instr.expLogica, ts)
    if val :
        ts_local = TS.TablaDeSimbolos(ts.simbolos)
        procesar_instrucciones(instr.instrIfVerdadero, ts_local)
    else :
        ts_local = TS.TablaDeSimbolos(ts.simbolos)
        procesar_instrucciones(instr.instrIfFalso, ts_local)

def resolver_cadena(expCad, ts) :
    if isinstance(expCad, ExpresionSimpleComilla) :
        return expCad.val
    elif isinstance(expCad, ExpresionNumerica) :
        return str(resolver_expresion_aritmetica(expCad, ts))
    else :
        print('Error: Expresión cadena no válida')


def resolver_expresion_logica(expLog, ts) :
    if isinstance(expLog,ExpresionLogica):
        exp1 = resolver_expresion_aritmetica(expLog.exp1, ts)
        exp2 = resolver_expresion_aritmetica(expLog.exp2, ts)
        if expLog.operador == OPERACION_LOGICA.AND : return exp1 and exp2
        if expLog.operador == OPERACION_LOGICA.OR : return exp1 or exp2
        if expLog.operador == OPERACION_LOGICA.XOR : return exp1 ^ exp2
    elif isinstance(expLog,ExpresionLogicaNot):
        exp = resolver_expresion_aritmetica(expLog.exp, ts)
        pivote=not exp
        if pivote==True: return 1
        else: return 0


def resolver_expresion_aritmetica(expNum, ts) :
    if isinstance(expNum, ExpresionAritmetica) :
        exp1 = resolver_expresion_aritmetica(expNum.exp1, ts)
        exp2 = resolver_expresion_aritmetica(expNum.exp2, ts)
        if expNum.operador == OPERACION_ARITMETICA.MAS : 
            if  re.match('-?\d+',str(exp1))  and re.match('-?\d+',str(exp2)):  return exp1 + exp2
            elif re.match('\".*?\"',str(exp1))  and re.match('\".*?\"',str(exp2)):  return exp1 + exp2
            else: 
                print("error: no se pueden operar distintos tipos")
                return 0
        if expNum.operador == OPERACION_ARITMETICA.MENOS : 
            if  re.match('-?\d+',str(exp1))  and re.match('-?\d+',str(exp2)):  return exp1 - exp2
            else: 
                print("error: no se pueden operar distintos tipos")
                return 0
        if expNum.operador == OPERACION_ARITMETICA.POR : 
            if  re.match('-?\d+',str(exp1))  and re.match('-?\d+',str(exp2)):  return exp1 * exp2
            else: 
                print("error: no se pueden operar distintos tipos")
                return 0
        
        if expNum.operador == OPERACION_ARITMETICA.DIVIDIDO : 
            if  re.match('-?\d+',str(exp1))  and re.match('-?\d+',str(exp2)): return exp1 / exp2
            else: 
                print("error: no se pueden operar distintos tipos")
                return 0
        if expNum.operador == OPERACION_ARITMETICA.RESIDUO : 
            if  re.match('-?\d+',str(exp1))  and re.match('-?\d+',str(exp2)): return exp1 % exp2
            else: 
                print("error: no se pueden operar distintos tipos")
                return 0
    elif isinstance(expNum, ExpresionNegativo) :
        exp = resolver_expresion_aritmetica(expNum.exp, ts)
        return exp * -1
    elif isinstance(expNum,ExpresionAbsoluto):
        exp= resolver_expresion_aritmetica(expNum.exp, ts)
        return abs(exp)
    elif isinstance(expNum, ExpresionNumero) :
        return expNum.val
    elif isinstance(expNum, ExpresionIdentificador) :
        return ts.obtener(expNum.id).valor
    elif isinstance(expNum,ExpresionSimpleComilla):
        return expNum.val
    

def resolver_expresion_bit(expBit,ts):
    if isinstance(expBit,ExpresionBit):
        exp1= resolver_expresion_aritmetica(expBit.exp1,ts)
        exp2= resolver_expresion_aritmetica(expBit.exp2,ts)
        if expBit.operador == OPERACION_BIT.AND : return exp1 and exp2
        if expBit.operador == OPERACION_BIT.OR : return exp1 or exp2
        if expBit.operador == OPERACION_BIT.XOR : return exp1 ^ exp2
        if expBit.operador == OPERACION_BIT.DESPLAZAMIENTO_IZQUIERDA : return exp1 << exp2
        if expBit.operador == OPERACION_BIT.DESPLAZAMIENTO_DERECHA : return exp1 >> exp2
    elif isinstance(expBit,ExpresionBitNot):
        exp = resolver_expresion_aritmetica(expBit.exp, ts)
        return (~ exp)

def resolver_casteo(expCast,ts):
    exp= resolver_expresion_aritmetica(expCast.exp,ts)
    if expCast.operador == OPERACION_CASTEO.ENTERO : return convertirEntero(exp)
    if expCast.operador == OPERACION_CASTEO.FLOTANTE : return convertirFlotante(exp)
    if expCast.operador == OPERACION_CASTEO.CARACTER : return convertirCaracter(exp)

def convertirEntero(valor):
    if  re.match('[a-zA-Z].*?',str(valor)): 
        if len(valor)>1:
            return ord(valor[0])
        else:
            return ord(valor)
    elif re.match('[0-9]+',str(valor)): 
        return int(valor)
    elif re.match('[0-9]+.[0-9]+',str(valor)): 
        return int(valor)
    else: 
        print("error: no se puede castear ese tipo de dato")       
    return 0

def convertirFlotante(valor):
    if  re.match('[a-zA-Z].*?',str(valor)): 
        if len(valor)>1:
            return float(ord(valor[0]))
        else:
            return float(ord(valor))
    elif re.match('[0-9]+',str(valor)): 
        return float(valor)
    elif re.match('[0-9]+.[0-9]+',str(valor)): 
        return float(valor)
    else: 
        print("error: no se puede castear ese tipo de dato")       
    return 0

def convertirCaracter(valor):
    if  re.match('[a-zA-Z].*?',str(valor)): 
        if len(valor)>1:
            return valor[0]
        else:
            return valor
    elif re.match(r'[0-9]+',str(valor)):
        return chr(int(valor))
    elif re.match('[0-9]+.[0-9]+',str(valor)): 
        return 0
    else: 
        print("error: no se puede castear ese tipo de dato")       
    return 0

def resolver_expresion_relacional(expRel,ts):
    exp1= resolver_expresion_aritmetica(expRel.exp1,ts)
    exp2= resolver_expresion_aritmetica(expRel.exp2,ts)
    if expRel.operador == OPERACION_RELACIONAL.IGUAL_IGUAL : return resolverLogica(exp1,exp2,1)
    if expRel.operador == OPERACION_RELACIONAL.NO_IGUAL : return resolverLogica(exp1,exp2,2)
    if expRel.operador == OPERACION_RELACIONAL.MAYOR_IGUAL : return resolverLogica(exp1,exp2,3)
    if expRel.operador == OPERACION_RELACIONAL.MENOR_IGUAL : return resolverLogica(exp1,exp2,4)
    if expRel.operador == OPERACION_RELACIONAL.MAYOR : return resolverLogica(exp1,exp2,5)
    if expRel.operador == OPERACION_RELACIONAL.MENOR : return resolverLogica(exp1,exp2,6)

def resolverLogica(op1,op2,operacion):
    if operacion==1:
        if(op1 == op2): return 1
        else: return 0
    if operacion==2:
        if(op1 != op2): return 1
        else: return 0
    if operacion==3:
        if(op1 >= op2): return 1
        else: return 0
    if operacion==4:
        if(op1 <= op2): return 1
        else: return 0
    if operacion==5:
        if(op1 > op2): return 1
        else: return 0
    if operacion==6:
        if(op1 < op2): return 1
        else: return 0
    else: return 1


def procesar_instrucciones(instrucciones, ts) :
    ## lista de instrucciones recolectadas
    for instr in instrucciones :
        if isinstance(instr, Imprimir) : procesar_imprimir(instr, ts)
        elif isinstance(instr,Asignacion): procesar_asignacion(instr,ts)
        elif isinstance(instr, If) : procesar_if(instr, ts)
        elif isinstance(instr,Salida): break
        else : print('Error: instrucción no válida')

def procesar_etiquetas(bloques,ts): 
    procesar_instrucciones(bloques,ts)



import gramaticaDescendente as g

def ejecucionDescendente(input,input2):
    h.textosalida=""
    h.textosalida=input2
    #print("--------------------------------Archivo original---------------------------------------")
    #print(input)
    print("--------------------------------Archivo Ejecucion---------------------------------------")
    prueba =g.parse(input)
    ts_global=TS.TablaDeSimbolos()
    procesar_etiquetas(prueba,ts_global)
    print("--------------------------------Reporte Gramatical---------------------------------------")
    #h.reporteGramatical()
    #h.graficarAST()

    #ts_global.mostrar(2)
    #for x in ts_global.simbolos:
     ##   print(x,"=",ts_global.obtener(x).valor,ts_global.obtener(x).tipo)
    
    return h.textosalida


def genenerarReporteGramaticalAscendente(ruta):
    h.reporteGramatical1=""
    h.reporteGramatical2=""
    h.reporteGramatical(ruta)

def genenerarReporteErrores(ruta):
    h.reporteErrores(ruta)