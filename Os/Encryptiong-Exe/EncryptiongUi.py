# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Hywell\Desktop\untitled.ui'
#
# Created: Fri Aug 18 15:35:18 2017
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from Encryptiong import Encryptiong

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class Ui_RSA(object):
    def setupUi(self, RSA):
        RSA.setObjectName(_fromUtf8("RSA"))
        RSA.resize(390, 156)
        self.pushButton = QtGui.QPushButton(RSA)
        self.pushButton.setGeometry(QtCore.QRect(300, 20, 75, 23))
        self.pushButton.setCheckable(True)
        self.pushButton.setChecked(True)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_2 = QtGui.QPushButton(RSA)
        self.pushButton_2.setGeometry(QtCore.QRect(300, 70, 75, 23))
        self.pushButton_2.setCheckable(True)
        self.pushButton_2.setChecked(True)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton_3 = QtGui.QPushButton(RSA)
        self.pushButton_3.setGeometry(QtCore.QRect(300, 120, 75, 23))
        self.pushButton_3.setCheckable(True)
        self.pushButton_3.setChecked(True)
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.lineEdit = QtGui.QLineEdit(RSA)
        self.lineEdit.setGeometry(QtCore.QRect(40, 30, 113, 20))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.lineEdit_2 = QtGui.QLineEdit(RSA)
        self.lineEdit_2.setGeometry(QtCore.QRect(40, 80, 113, 20))
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.label = QtGui.QLabel(RSA)
        self.label.setGeometry(QtCore.QRect(40, 10, 54, 12))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(RSA)
        self.label_2.setGeometry(QtCore.QRect(40, 60, 54, 12))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        # self.progressBar = QtGui.QProgressBar(RSA)
        # self.progressBar.setGeometry(QtCore.QRect(40, 130, 151, 23))
        # self.progressBar.setProperty("value", 0)
        # self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.label_3 = QtGui.QLabel(RSA)
        self.label_3.setGeometry(QtCore.QRect(40, 110, 54, 12))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        
        self.pushButton.clicked.connect(lambda : self.work(1))  # 只有单击才会调用 设置匿名函数 
        self.pushButton_2.clicked.connect(lambda : self.work(2))
        self.pushButton_3.clicked.connect(lambda : self.work(3))
        
        self.retranslateUi(RSA)
        QtCore.QMetaObject.connectSlotsByName(RSA)

    def work(self, Ctype):
        try:
            if Ctype == 1:
                Encryptiong().encryp()
                QtGui.QMessageBox.about( self, u'提醒', u"成功生成公、私钥文件！")
            elif Ctype == 2:
                public = str(self.lineEdit.text())  # 获取line的文本
                filepath = str(self.lineEdit_2.text())  # 获取line2的文本
                Encryptiong(public=public, filepath=filepath).encryption()
                QtGui.QMessageBox.about(self, u'提醒', u"完成加密！")
            elif Ctype == 3:
                private = str(self.lineEdit.text())
                filepath = str(self.lineEdit_2.text())
                Encryptiong(private=private,decrypt=filepath).decrypted()
                QtGui.QMessageBox.about(self, u'提醒', u"完成解密！")
        except:
            QtGui.QMessageBox.about(self, u'警告', u"输入有误,请重新输入！")
        
    def retranslateUi(self, RSA):
        RSA.setWindowTitle(_translate("RSA", "RSA加密程序", None))
        self.pushButton.setText(_translate("RSA", "生成钥文件", None))
        self.pushButton_2.setText(_translate("RSA", "加密", None))
        self.pushButton_3.setText(_translate("RSA", "解密", None))
        self.label.setText(_translate("RSA", "钥文件", None))
        self.label_2.setText(_translate("RSA", "工作目录", None))
        # self.label_3.setText(_translate("RSA", "工作进度", None))
