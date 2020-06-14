from PyQt5 import QtCore, QtGui, QtWidgets
#from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
import accionesIDE as accionesVarias
import mostrarLineas
from random import seed
from random import randint


class SyntaxHighlighter(QtGui.QSyntaxHighlighter):
    def __init__(self, parent):
        super(SyntaxHighlighter, self).__init__(parent)
        self._highlight_lines = dict()

    def highlight_line(self, line, fmt):
        if isinstance(line, int) and line >= 0 and isinstance(fmt, QtGui.QTextCharFormat):
            self._highlight_lines[line] = fmt
            tb = self.document().findBlockByLineNumber(line)
            self.rehighlightBlock(tb)

    def clear_highlight(self):
        self._highlight_lines = dict()
        self.rehighlight()

    def highlightBlock(self, text):
        line = self.currentBlock().blockNumber()
        fmt = self._highlight_lines.get(line)
        if fmt is not None:
            self.setFormat(0, len(text), fmt)


#clase central de mi ventana a mostrarse
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        c=accionesVarias.accionesIde()
        MainWindow.setObjectName("MainWindow")
        #tamaño que tendra la ventana 1400px x 900px
        MainWindow.resize(1400, 900)
        #le indico que se abra desde el centro de la pantalla pooniendolo en el objeto ventanaCentrada
        self.ventanaCentrada = QtWidgets.QWidget(MainWindow)
        self.ventanaCentrada.setObjectName("ventanaCentrada")
        #se crea etiqueta
        #self.EdicionTexto = QtWidgets.QPlainTextEdit(self.ventanaCentrada)
        self.EdicionTexto = mostrarLineas.QCodeEditor(self.ventanaCentrada)
        #para definir su posicion
        self.EdicionTexto.setGeometry(QtCore.QRect(40, 70, 860, 500))
        font = QtGui.QFont()
        # para cambiar el tamaño de la fuente de un objeto
        font.setPointSize(16)
        self.EdicionTexto.setFont(font)
        self.EdicionTexto.setObjectName("EdicionTexto")

        #area del debugger
        self.DebugTexto = QtWidgets.QPlainTextEdit(self.ventanaCentrada)
        self.DebugTexto.setGeometry(QtCore.QRect(930, 70, 450, 500))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.DebugTexto.setFont(font)
        self.DebugTexto.setObjectName("DebugTexto")

        #area de consola de salida
        self.ConsolaSalida = QtWidgets.QTextEdit(self.ventanaCentrada)
        self.ConsolaSalida.setGeometry(QtCore.QRect(40, 590, 1340, 260))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.ConsolaSalida.setFont(font)
        self.ConsolaSalida.setObjectName("ConsolaSalida")

        MainWindow.setCentralWidget(self.ventanaCentrada)
        #fijo la barra de menu en la parte superior
        self.barraMenu = QtWidgets.QMenuBar(MainWindow)
        self.barraMenu.setGeometry(QtCore.QRect(0, 0, 800, 36))
        self.barraMenu.setObjectName("barraMenu")
        #archivo
        self.archivoMenu = QtWidgets.QMenu(self.barraMenu)
        self.archivoMenu.setObjectName("archivoMenu")
        #editar
        self.editarMenu = QtWidgets.QMenu(self.barraMenu)
        self.editarMenu.setObjectName("editarMenu")
        #ejecutar
        self.ejecutarMenu = QtWidgets.QMenu(self.barraMenu)
        self.ejecutarMenu.setObjectName("ejecutarMenu")
        #opciones
        self.opcionesMenu = QtWidgets.QMenu(self.barraMenu)
        self.opcionesMenu.setObjectName("opcionesMenu")
        #ayuda
        self.ayudaMenu = QtWidgets.QMenu(self.barraMenu)
        self.ayudaMenu.setObjectName("ayudaMenu")
        #etiquetas de iconos
        self.iconoAbrir = QtWidgets.QPushButton(self.ventanaCentrada)
        self.iconoAbrir.setGeometry(QtCore.QRect(40, 10, 50, 50))
        self.iconoAbrir.setObjectName("iconoAbrir")
        
        #self._lineedit = QtWidgets.QLineEdit()
        self.textoBusqueda = QtWidgets.QLineEdit(self.ventanaCentrada)
        self.textoBusqueda.setGeometry(QtCore.QRect(700, 10, 200, 30))
        self.textoBusqueda.setObjectName("textoBusqueda")
        
        self.textoReemplazo = QtWidgets.QLineEdit(self.ventanaCentrada)
        self.textoReemplazo.setGeometry(QtCore.QRect(930, 10, 200, 30))
        self.textoReemplazo.setObjectName("textoBusqueda")

        self._highlighter = SyntaxHighlighter(self.EdicionTexto.document())

        self.iconoNuevo = QtWidgets.QPushButton(self.ventanaCentrada)
        self.iconoNuevo.setGeometry(QtCore.QRect(90, 10, 50, 50))
        self.iconoNuevo.setObjectName("iconoNuevo")

        self.iconoGuardar = QtWidgets.QPushButton(self.ventanaCentrada)
        self.iconoGuardar.setGeometry(QtCore.QRect(140, 10, 50, 50))
        self.iconoGuardar.setObjectName("iconoGuardar")

        self.iconoGuardarComo = QtWidgets.QPushButton(self.ventanaCentrada)
        self.iconoGuardarComo.setGeometry(QtCore.QRect(190, 10, 50, 50))
        self.iconoGuardarComo.setObjectName("iconoGuardarComo")

        self.iconoDescendente = QtWidgets.QPushButton(self.ventanaCentrada)
        self.iconoDescendente.setGeometry(QtCore.QRect(300, 10, 50, 50))
        self.iconoDescendente.setObjectName("iconoDescendente")

        self.iconoAscendente = QtWidgets.QPushButton(self.ventanaCentrada)
        self.iconoAscendente.setGeometry(QtCore.QRect(350, 10, 50, 50))
        self.iconoAscendente.setObjectName("iconoAscendente")

        self.iconoDebug = QtWidgets.QPushButton(self.ventanaCentrada)
        self.iconoDebug.setGeometry(QtCore.QRect(400, 10, 50, 50))
        self.iconoDebug.setObjectName("iconoDebug")


        #------------------------------------------------
        MainWindow.setMenuBar(self.barraMenu)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        #acciones de Archivo
        self.accionNuevo = QtWidgets.QAction(MainWindow)
        self.accionNuevo.setObjectName("accionNuevo")
        self.accionAbrir = QtWidgets.QAction(MainWindow)
        self.accionAbrir.setObjectName("accionAbrir")
        self.accionGuardar = QtWidgets.QAction(MainWindow)
        self.accionGuardar.setObjectName("accionGuardar")
        self.accionGuardarComo = QtWidgets.QAction(MainWindow)
        self.accionGuardarComo.setObjectName("accionGuardarComo")
        self.accionCerrar = QtWidgets.QAction(MainWindow)
        self.accionCerrar.setObjectName("accionCerrar")
        self.accionSalir = QtWidgets.QAction(MainWindow)
        self.accionSalir.setObjectName("accionSalir")
        
        self.archivoMenu.addAction(self.accionNuevo)
        self.archivoMenu.addAction(self.accionAbrir)
        self.archivoMenu.addAction(self.accionGuardar)
        self.archivoMenu.addAction(self.accionGuardarComo)
        self.archivoMenu.addAction(self.accionCerrar)
        self.archivoMenu.addAction(self.accionSalir)
        #acciones de editar
        self.accionBuscar = QtWidgets.QAction(MainWindow)
        self.accionBuscar.setObjectName("accionBuscar")
        self.accionReemplazar = QtWidgets.QAction(MainWindow)
        self.accionReemplazar.setObjectName("accionReemplazar")


        self.editarMenu.addAction(self.accionBuscar)
        self.editarMenu.addAction(self.accionReemplazar)
        #acciones Ejecutar
        self.accionDescendente = QtWidgets.QAction(MainWindow)
        self.accionDescendente.setObjectName("accionDescendente")
        self.accionAscendente = QtWidgets.QAction(MainWindow)
        self.accionAscendente.setObjectName("accionAscendente")
        self.accionPasos = QtWidgets.QAction(MainWindow)
        self.accionPasos.setObjectName("accionPasos")
        self.accionSimbolos = QtWidgets.QAction(MainWindow)
        self.accionSimbolos.setObjectName("accionsimbolos")
        self.accionAST = QtWidgets.QAction(MainWindow)
        self.accionAST.setObjectName("accionAST")
        self.accionGramatical = QtWidgets.QAction(MainWindow)
        self.accionGramatical.setObjectName("accionGramatical")
        self.accionErrores = QtWidgets.QAction(MainWindow)
        self.accionErrores.setObjectName("accionErrores")

        self.ejecutarMenu.addAction(self.accionDescendente)
        self.ejecutarMenu.addAction(self.accionAscendente)
        self.ejecutarMenu.addAction(self.accionPasos)
        self.ejecutarMenu.addAction(self.accionSimbolos)
        self.ejecutarMenu.addAction(self.accionAST)
        self.ejecutarMenu.addAction(self.accionGramatical)
        self.ejecutarMenu.addAction(self.accionErrores)
        #acciones de opciones
        self.accionColor = QtWidgets.QAction(MainWindow)
        self.accionColor.setObjectName("accionColor")
        self.accionLinea = QtWidgets.QAction(MainWindow)
        self.accionLinea.setObjectName("accionLinea")

        self.opcionesMenu.addAction(self.accionColor)
        self.opcionesMenu.addAction(self.accionLinea)
        #acciones de ayuda y acerca de
        self.accionAyuda = QtWidgets.QAction(MainWindow)
        self.accionAyuda.setObjectName("accionAyuda")
        self.accionAcerca = QtWidgets.QAction(MainWindow)
        self.accionAcerca.setObjectName("accionAcerca")

        self.ayudaMenu.addAction(self.accionAyuda)
        self.ayudaMenu.addAction(self.accionAcerca)
        #genera los botones y su accion de despliegue
        self.barraMenu.addAction(self.archivoMenu.menuAction())
        self.barraMenu.addAction(self.editarMenu.menuAction())
        self.barraMenu.addAction(self.ejecutarMenu.menuAction())
        self.barraMenu.addAction(self.opcionesMenu.menuAction())
        self.barraMenu.addAction(self.ayudaMenu.menuAction())
        #acciones de los botones de cada menu
        
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        #funciones de archivo
        self.accionNuevo.triggered.connect(lambda: self.EdicionTexto.insertPlainText(""))
        self.accionAbrir.triggered.connect(self.abrir_archivo)
        self.accionGuardar.triggered.connect(lambda: self.guardar_normal(self.EdicionTexto.toPlainText()))
        self.accionGuardarComo.triggered.connect(lambda: self.guardar_como(self.EdicionTexto.toPlainText()))
        self.accionCerrar.triggered.connect(lambda: c.cerrarVentana(QtWidgets.QApplication(sys.argv)))
        self.accionSalir.triggered.connect(lambda: c.cerrarVentana(QtWidgets.QApplication(sys.argv)))
        #funciones de editar
        self.accionBuscar.triggered.connect(self.onTextChanged)
        self.accionReemplazar.triggered.connect(self.buscarReemplazar)
        #funciones de ejecutar

        #funciones de opciones
        self.accionColor.triggered.connect(lambda: self.cambiarColor())
        #funciones de ayuda
        self.accionAcerca.triggered.connect(lambda: self.ventanaAcercaDe("hola"))
        #acciones de los botoncitos destemplados :v



        self.iconoAbrir.clicked.connect(self.abrir_archivo)
        self.iconoGuardar.clicked.connect(self.guardar_normal)
        self.iconoGuardarComo.clicked.connect(self.guardar_como)
        self.iconoDescendente.clicked.connect(self.ejecutar_descendente)
        self.iconoAscendente.clicked.connect(self.ejecutar_ascendente)
        #self.iconoDebug.clicked.connect(self.abrir_archivo)
        self.iconoNuevo.clicked.connect(lambda: self.EdicionTexto.insertPlainText(""))

    def retranslateUi(self, MainWindow):
        #aca solo setteo los nombres en cada componente y un sub nombre por asi decirlo
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Augus - Jossie Castrillo 201313692"))
        self.EdicionTexto.insertPlainText(_translate("MainWindow", ""))
        self.archivoMenu.setTitle(_translate("MainWindow", "Archivo"))
        self.editarMenu.setTitle(_translate("MainWindow", "Editar"))
        self.ejecutarMenu.setTitle(_translate("MainWindow", "Ejecutar"))
        self.opcionesMenu.setTitle(_translate("MainWindow", "Opciones"))
        self.ayudaMenu.setTitle(_translate("MainWindow", "Ayuda"))
        #de editar
        self.accionBuscar.setText(_translate("MainWindow", "Buscar"))
        self.accionReemplazar.setText(_translate("MainWindow", "Reemplazar"))
        # de archivo
        self.accionNuevo.setText(_translate("MainWindow", "Nuevo"))
        self.accionNuevo.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.accionAbrir.setText(_translate("MainWindow", "Abrir"))
        self.accionAbrir.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.accionGuardar.setText(_translate("MainWindow", "Guardar"))
        self.accionGuardar.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.accionGuardarComo.setText(_translate("MainWindow", "Guardar Como"))
        self.accionGuardarComo.setShortcut(_translate("MainWindow", "Ctrl+P"))
        self.accionCerrar.setText(_translate("MainWindow", "Cerrar"))
        self.accionCerrar.setShortcut(_translate("MainWindow", "Ctrl+W"))
        self.accionSalir.setText(_translate("MainWindow", "Salir"))
        self.accionSalir.setShortcut(_translate("MainWindow", "Ctrl+E"))
        #de ejecutar
        self.accionDescendente.setText(_translate("MainWindows","Analisis Descendente"))
        self.accionAscendente.setText(_translate("MainWindows","Analisis Ascendente"))
        self.accionPasos.setText(_translate("MainWindows","Analisis paso a paso"))
        self.accionSimbolos.setText(_translate("MainWindows","Tabla de simbolos"))
        self.accionAST.setText(_translate("MainWindows","AST"))
        self.accionGramatical.setText(_translate("MainWindows","Reporte Gramatical"))
        self.accionErrores.setText(_translate("MainWindows","Reporte de Errores"))
        #de opciones
        self.accionColor.setText(_translate("MainWindows","Cambiar color"))
        self.accionLinea.setText(_translate("MainWindows","Cambiar Numeracion"))
        #de ayuda
        self.accionAyuda.setText(_translate("MainWindows","Ayuda"))
        self.accionAcerca.setText(_translate("MainWindows","Acerca de"))

        self.iconoAbrir.setText(_translate("MainWindows","Open"))
        self.iconoNuevo.setText(_translate("MainWindows","nuevo"))
        self.iconoGuardar.setText(_translate("MainWindows","save"))
        self.iconoGuardarComo.setText(_translate("MainWindows","save as"))
        self.iconoDescendente.setText(_translate("MainWindows","desc"))
        self.iconoAscendente.setText(_translate("MainWindows","asc"))
        self.iconoDebug.setText(_translate("MainWindows","debug"))
        self.textoBusqueda.setText(_translate("MainWindows","buscar"))
        self.textoReemplazo.setText(_translate("MainWindows","reemplazar"))

#self.EdicionTexto.setText(c.abrirArchivo("C:\\Users\\Jossie Castrillo\\Desktop\\[OLC2]P1_201313692\\prueba.txt"))
    def clicked(self, text):
        self.EdicionTexto.insertPlainText(path)
        print(path)
        #self.EdicionTexto.adjustSize()
    #metodo para cambiar el color del fondo del entorno de escritura unicamente (falta mejorar)
    def cambiarColor(self):
        valor=randint(0,10)
        print(valor)
        if valor %2 ==0:
            self.EdicionTexto.setStyleSheet("background: white")
        else:
            self.EdicionTexto.setStyleSheet("background: grey")
    #metodo para mostrar la ventana emergente con los datos del desarrollador, osea yo
    def ventanaAcercaDe(self,t):
        print(t)
        msg=QtWidgets.QMessageBox()
        msg.setWindowTitle("Acerca De...")
        msg.setText("Jossie Bismarck Castrillo Fajardo - 201313692")
        msg.exec_()
    #metodo para ventana emergente generica
    def ventanaEmergente(self,mensaje):
        msg=QtWidgets.QMessageBox()
        msg.setWindowTitle("Notificacion")
        msg.setText(mensaje)
        msg.exec_()
    #este metodo genera el file chooser donde se podra buscar el archivo y devuelve la ruta del archivo
    #posteriormente se manda la ruta el meetodo c.abrirArchivo del import accionesIDE y devuelve el texto abierto
    def abrir_archivo(self):
        try:
            c=accionesVarias.accionesIde()
            dialog = QtWidgets.QFileDialog()
            fname = dialog.getOpenFileName(None, "Abrir archivo", "", "all (*.*)")
            global path
            path=fname[0]
            self.EdicionTexto.insertPlainText(c.abrirArchivo(path))
            print(path)
        except:
            self.ventanaEmergente("no se selecciono ningun archivo")
    #envia el texto del editor y la ruta de un archivo ya abierto al metodo del import accionesIDE de guardarArchivo
    def guardar_como(self,texto):
        try:
            c=accionesVarias.accionesIde()
            name = QtWidgets.QFileDialog.getSaveFileName(None, 'Save File')
            print(name[0])
            if c.guardarArchivo(name[0],texto):
                self.ventanaEmergente("Se ha guardado su archivo exitosamente!")
            #abre un file chooser para seleccionar un lugar para guardar el archivo y permite escribir el nombre con su extension.
            #esa ruta se envia con el texto del editor al metodo guardarArchivo
        except:
            self.ventanaEmergente("no se guardo el archivo")
    def guardar_normal(self,texto):
        try:
            c=accionesVarias.accionesIde()
            if c.guardarArchivo(path,texto):
                self.ventanaEmergente("Se ha guardado su archivo exitosamente!")
        except:
            self.ventanaEmergente("la ruta no se ha definido")


    def ejecutar_ascendente(self):
        x=self.EdicionTexto.toPlainText()
        print(x)

        
        #print(x)
    
    def ejecutar_descendente(self):
        x=self.EdicionTexto.toPlainText()
        print(x)


    def onTextChanged(self):
            contador=0
            text=self.textoBusqueda.text()
            print("entrada: ",text)

            #probando devolver filas
            x=self.EdicionTexto.toPlainText()
            y=x.splitlines( )

            print("X es: ",x.splitlines( ))
            fmt = QtGui.QTextCharFormat()
            fmt.setBackground(QtGui.QColor("red"))
            self._highlighter.clear_highlight()
            for i in y:
                contador+=1
                if text in i:
                    print(i,"-----",contador-1)
                    #print(contador)
                    self._highlighter.highlight_line(contador-1, fmt)

    def buscarReemplazar(self):
        texto=self.EdicionTexto.toPlainText()
        buscada=self.textoBusqueda.text()
        reemplazo=self.textoReemplazo.text()
        nuevaCadena= texto.replace(buscada, reemplazo)
        self.EdicionTexto.setPlainText(nuevaCadena)



#inicializacion del main y su interfaz para ejecucion
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())