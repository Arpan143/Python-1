# -*- coding: utf-8 -*-
from PyQt4.QtGui import *  
from PyQt4 import QtGui
from PyQt4.QtCore import *  
import sys  
import EncryptiongUi

  
class RsaDlg(QDialog, EncryptiongUi.Ui_RSA):  # 将EncryptiongUi文件的UI_RSA类传递
    def __init__(self, parent=None):  
        super(RsaDlg, self).__init__(parent)  
        self.setupUi(self)  
        self.setWindowIcon(QtGui.QIcon('./ico.ico'))  # 设置icon


def main():
    app = QApplication(sys.argv)  
    dialog = RsaDlg()
    dialog.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()
