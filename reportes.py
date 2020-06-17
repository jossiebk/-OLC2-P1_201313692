# -----------------------------------------------------------------------------
#                      REPORTE GRAMATICAL
# -----------------------------------------------------------------------------
global textosalida
textosalida=""
global reporteGramatical1
global reporteGramatical2
reporteGramatical1=" "
reporteGramatical2 = " "


def invertir_cadena_manual(cadena):
    cadena_invertida = ""
    x=cadena.splitlines(True)
    x.reverse()
    for line in x:
        cadena_invertida = cadena_invertida + line +"<br>"
    print(cadena_invertida)
    return cadena_invertida


def reporteGramatical(ruta):
    var1= invertir_cadena_manual(reporteGramatical1)
    var2= invertir_cadena_manual(reporteGramatical2)
    var3="""<h1>REPORTE GRAMAICAL<h1>
    <table>
  <tr>
    <td>Producciones</td>
    <td>Reglas Semanticas</td>
  </tr>
  <tr>
    <td>"""+var1+ """</td>
    <td>"""+var2+"""</td>
  </tr>
</table> """
    with open(ruta+".html", "w") as f:
        f.write(var3)
        f.closed

# -----------------------------------------------------------------------------
#                       REPORTE AST MAS O MENOS
# -----------------------------------------------------------------------------

import os
import graphviz as t
global ast
global prueba

def graficarAST():
    ast="""digraph {
        A [label="King Arthur"]
        B [label="Sir Bedevere the Wise"]
        L [label="Sir Lancelot the Brave"]
        A -> B
        A -> L
        B -> L [constraint=false]
    }
    """
    with open("C:\\Users\\Jossie Castrillo\\Desktop\\ast1.dot", "w") as f:
        f.write(ast)
        f.closed
    t.render('dot', 'png', 'C:\\Users\\Jossie Castrillo\\Desktop\\ast1.dot')

    #cmd='"C:\\Program Files (x86)\\Graphviz2.38\\bin\\dot.exe" -Tjpg C:\\Users\\Jossie Castrillo\\Desktop\\ast1.dot -o C:\\Users\\Jossie Castrillo\\Desktop\\ast1.jpg'
    #os.system(cmd)
# -----------------------------------------------------------------------------
#                       REPORTE DE ERRORES
# -----------------------------------------------------------------------------

global filapivote
filapivote=0
global errores
errores=""
def reporteErrores(ruta):
    var3="""<h1>REPORTE GRAMAICAL<h1>
    <table>
    <tr>
    <td>ERROR</td>
    <td>FILA</td>
    <td>COLUMNA</td>
    <td>TIPO</td>
    <td>MENSAJE</td>
    </tr>"""+errores+"""</table> """
    with open(ruta+".html", "w") as f:
        f.write(var3)
        f.closed

        

global todo
todo=[]

global q
q=[]
def insertarSimbolos(var):
    for i in q:
        if i==0:
            q.append(var)
            #print("numeral ",i)
            return


# -----------------------------------------------------------------------------
#                       LA PODEROSA TABLA DE SIMBOLOS :V
# -----------------------------------------------------------------------------


def reporteSimbolos(ruta,cadena):
    print(cadena)
    print(ruta)
    ar3="""<h1>REPORTE TABLA DE SIMBOLOS<h1>
    <table>
    <tr>
    <td>ID</td>
    <td>VALOR</td>
    <td>TIPO</td>
    </tr>"""+cadena+"""</table> """
    print("forma bien la cadena")
    with open(ruta+".html", "w") as f:
        f.write(ar3)
        f.closed