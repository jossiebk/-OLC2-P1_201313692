import gramaticaAscendente as g
import gramaticaAscendente as gr
import re
import tablaDeSimbolos as TS
from expresiones import *
from instrucciones import *
import reportes as h




def procesar_imprimir(instr, ts) :
    cadena=resolver_cadena(instr.cad, ts)
    a=""
    if cadena.count('\\n')>0:
        print('Jossie>', resolver_cadena(instr.cad, ts).replace("\\n","\nJossie>"))
        a="Jossie>"
        a+=resolver_cadena(instr.cad, ts).replace("\\n","\nJossie>")
        a+="\n"
        h.textosalida+=a
    else:
        print('Jossie>', resolver_cadena(instr.cad, ts))
        a="Jossie>"
        a+=resolver_cadena(instr.cad, ts)
        a+="\n"
        h.textosalida+=a

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
    print("entra al if")
    print("la expresion logica es:   ",instr.expLogica)
    val = resolver_expresion_relacional(instr.expLogica, ts)
    print("val es:   ",val)
    if val==1:
        procesar_salto_if(instr.instrIfFalso,ts)

def procesar_salto_if(instr,ts):
    print(h.todo)
    for i in h.todo:
        print("====> ",i)
        a=i[0]
        b=i[1]
        print(a)
        print(b)
        if a==instr :
            print("encuentra la etiqueta")
            procesar_instrucciones(b,ts)
        else:
            print("nel")
            #procesar_instrucciones(b,ts)




def resolver_cadena(expCad, ts) :
    if isinstance(expCad, ExpresionSimpleComilla) :
        return expCad.val
    elif isinstance(expCad, ExpresionNumerica) :
        return str(resolver_expresion_aritmetica(expCad, ts))
    else :
        print('Error: Expresión cadena no válida')
        h.errores+=  "<tr><td>"+str(expCad)+"</td><td>N/A</td><td>N/A</td><td>SEMANTICO</td><td>expresion no valida</td></tr>\n"
        return 'Error: expresion no valida'


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
                h.errores+=  "<tr><td>"+str(exp1)+"|"+str(exp2)+ "</td><td>N/A</td><td>N/A</td><td>SEMANTICO</td><td>no se pueden operar distintos tipos</td></tr>\n"
                return 0
        if expNum.operador == OPERACION_ARITMETICA.MENOS : 
            if  re.match('-?\d+',str(exp1))  and re.match('-?\d+',str(exp2)):  return exp1 - exp2
            else: 
                print("error: no se pueden operar distintos tipos")
                h.errores+=  "<tr><td>"+str(exp1)+"|"+str(exp2)+ "</td><td>N/A</td><td>N/A</td><td>SEMANTICO</td><td>no se pueden operar distintos tipos</td></tr>\n"
                return 0
        if expNum.operador == OPERACION_ARITMETICA.POR : 
            if  re.match('-?\d+',str(exp1))  and re.match('-?\d+',str(exp2)):  return exp1 * exp2
            else: 
                print("error: no se pueden operar distintos tipos")
                h.errores+=  "<tr><td>"+str(exp1)+"|"+str(exp2)+ "</td><td>N/A</td><td>N/A</td><td>SEMANTICO</td><td>no se pueden operar distintos tipos</td></tr>\n"
                return 0
        
        if expNum.operador == OPERACION_ARITMETICA.DIVIDIDO : 
            if  re.match('-?\d+',str(exp1))  and re.match('-?\d+',str(exp2)): return exp1 / exp2
            else: 
                print("error: no se pueden operar distintos tipos")
                h.errores+=  "<tr><td>"+str(exp1)+"|"+str(exp2)+ "</td><td>N/A</td><td>N/A</td><td>SEMANTICO</td><td>no se pueden operar distintos tipos</td></tr>\n"
                return 0
        if expNum.operador == OPERACION_ARITMETICA.RESIDUO : 
            if  re.match('-?\d+',str(exp1))  and re.match('-?\d+',str(exp2)): return exp1 % exp2
            else: 
                print("error: no se pueden operar distintos tipos")
                h.errores+=  "<tr><td>"+str(exp1)+"|"+str(exp2)+ "</td><td>N/A</td><td>N/A</td><td>SEMANTICO</td><td>no se pueden operar distintos tipos</td></tr>\n"
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
    else:
        h.errores+=  "<tr><td>"+str(exp1)+"|"+str(exp2)+ "</td><td>N/A</td><td>N/A</td><td>SEMANTICO</td><td>error de operacion</td></tr>\n"
    

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
        h.errores+=  "<tr><td>"+str(valor)+ "</td><td>N/A</td><td>N/A</td><td>SEMANTICO</td><td>no se puede castear ese tipo de dato</td></tr>\n"      
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
        h.errores+=  "<tr><td>"+str(valor)+ "</td><td>N/A</td><td>N/A</td><td>SEMANTICO</td><td>no se puede castear ese tipo de dato</td></tr>\n"        
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
        h.errores+=  "<tr><td>"+str(valor)+ "</td><td>N/A</td><td>N/A</td><td>SEMANTICO</td><td>no se puede castear ese tipo de dato</td></tr>\n"       
    return 0

def resolver_expresion_relacional(expRel,ts):
    print("entro a RELACIONAL")
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
        elif isinstance(instr,Goto) : procesar_salto(instr,ts)
        #elif
        else : 
            print('Error: instrucción no válida')
            h.errores+=  "<tr><td>"+str(instr)+ "</td><td>N/A</td><td>N/A</td><td>SEMANTICO</td><td>la instruccion no es valida</td></tr>\n"  

def procesar_salto(instr,ts):
    a=instr.etiqueta
    print(a)
    print(len(h.todo))
    for i in h.todo:
        b=i[0]
        c=i[1]
        if a==b:
            procesar_instrucciones(c,ts)
            print("tag del momento: ",i)
    else:
        print("La etiqueta o metodo no existe")


def procesar_etiquetas(ts,tag):
    print(h.todo)
    for i in h.todo:
        print("====> ",i)
        a=i[0]
        b=i[1]
        print(a)
        print(b)
        if a==tag :
            print("entra al main")
            procesar_instrucciones(b,ts)
            
        else:
            print("nel")
            #procesar_instrucciones(b,ts)



def ejecucionAscendente(input,input2):
    h.textosalida=""
    h.textosalida=input2
    h.q.clear()
    #print("--------------------------------Archivo original---------------------------------------")
    #print(input)
    print("--------------------------------Archivo Ejecucion---------------------------------------")
    prueba =g.parse(input)
    ts_global=TS.TablaDeSimbolos()
    h.todo=prueba
    print("--------------------------------divisor---------------------------------------------------")
    procesar_etiquetas(ts_global,"main")
    print("--------------------------------Reporte simbolos---------------------------------------")
    #ts_global.mostrar(2)
    for x in ts_global.simbolos:
       print(x,"=",ts_global.obtener(x).valor,ts_global.obtener(x).tipo)
    
    return h.textosalida


def genenerarReporteGramaticalAscendente(ruta):
    h.reporteGramatical(ruta)

def genenerarReporteErrores(ruta):
    h.reporteErrores(ruta)

#f = open("C:\\Users\\Jossie Castrillo\\Desktop\\ArchivosDePrueba\\pruebaj.txt", "r")
#input = f.read()

#--------------------------------------------------------------------------------------------------------------------------------------------------
#                    INVOCO GRAMATICA DESCENDENTE :V
#--------------------------------------------------------------------------------------------------------------------------------------------------
def ejecucionDescendente(input,input2):
    h.textosalida=""
    h.textosalida=input2
    h.q.clear()
    #print("--------------------------------Archivo original---------------------------------------")
    #print(input)
    print("--------------------------------Archivo Ejecucion---------------------------------------")
    prueba =gr.parse(input)
    ts_global=TS.TablaDeSimbolos()
    h.todo=prueba
    print("--------------------------------divisor---------------------------------------------------")
    procesar_etiquetas(ts_global,"main")
    print("--------------------------------Reporte Gramatical---------------------------------------")
    #h.reporteGramatical()
    #h.graficarAST()

    #ts_global.mostrar(2)
    #for x in ts_global.simbolos:
     ##   print(x,"=",ts_global.obtener(x).valor,ts_global.obtener(x).tipo)
    return h.textosalida


def genenerarReporteGramaticalDescendente(ruta):
    h.reporteGramatical(ruta)

def genenerarReporteErroresDescendente(ruta):
    h.reporteErrores(ruta)
