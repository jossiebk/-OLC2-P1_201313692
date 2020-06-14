
import sys
from PyQt5 import QtCore, QtGui, QtWidgets



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


class Widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)

        self._lineedit = QtWidgets.QLineEdit()


        self._plaintextedit = QtWidgets.QPlainTextEdit()

        self._highlighter = SyntaxHighlighter(self._plaintextedit.document())

        lay = QtWidgets.QVBoxLayout(self)
        lay.addWidget(self._lineedit)
        lay.addWidget(self._plaintextedit)

        for i in range(10):
            self._plaintextedit.appendPlainText("line %d" % i)

        self.resize(320, 240)

        self.boton = QtWidgets.QPushButton()
        self.boton.setGeometry(QtCore.QRect(40, 10, 50, 50))
        self.boton.setObjectName("boton")
        lay.addWidget(self.boton)
        
        self.boton.clicked.connect(self.onTextChanged)

    
    def onTextChanged(self):
        contador=0
        text=self._lineedit.text()
        print("entrada: ",text)

        #probando devolver filas
        x=self._plaintextedit.toPlainText()
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



if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec_())