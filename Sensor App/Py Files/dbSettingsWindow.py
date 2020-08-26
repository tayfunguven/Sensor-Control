from PyQt5 import QtCore, QtGui, QtWidgets
import configparser
import requests
import win32api
class Ui_databaseSettings(object):
    def dbCred (self, text):
        try:
            config = configparser.ConfigParser()
            config.read('config.ini')
            config.set("Database_settings","cred",text)
    
            with open('config.ini','w') as configfile:
                config.write(configfile)
        except Exception as x:
            win32api.MessageBox(0,f'An error occured! \n {x}','Error occured',0x00000010)
    def dbUrl (self, text):
        try:
            config = configparser.ConfigParser()
            config.read('config.ini')
            config.set("Database_settings","databaseurl",text)
        
            with open('config.ini','w') as configfile:
                    config.write(configfile)
        except Exception as x:
            win32api.MessageBox(0,f'An error occured! \n {x}','Error occured',0x00000010)
    def dbRef (self, text):
        try:
            config = configparser.ConfigParser()
            config.read('config.ini')
            config.set("Database_settings","databasereferance",text)
        
            with open('config.ini','w') as configfile:
                config.write(configfile)
        except Exception as x:
            win32api.MessageBox(0,f'An error occured! \n {x}','Error occured',0x00000010)

    def setupUi(self, databaseSettings):
        databaseSettings.setObjectName("databaseSettings")
        databaseSettings.setWindowModality(QtCore.Qt.WindowModal)
        databaseSettings.resize(500, 200)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(databaseSettings.sizePolicy().hasHeightForWidth())
        databaseSettings.setSizePolicy(sizePolicy)
        databaseSettings.setMaximumSize(QtCore.QSize(500, 200))
        databaseSettings.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("databaseIcon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        databaseSettings.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(databaseSettings)
        self.gridLayout.setObjectName("gridLayout")
        self.dbGroupBox = QtWidgets.QGroupBox(databaseSettings)
        self.dbGroupBox.setObjectName("dbGroupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.dbGroupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.lblCred = QtWidgets.QLabel(self.dbGroupBox)
        self.lblCred.setObjectName("lblCred")
        self.gridLayout_2.addWidget(self.lblCred, 0, 0, 1, 1)
        self.lineCred = QtWidgets.QLineEdit(self.dbGroupBox)
        self.lineCred.setText("")
        self.lineCred.setObjectName("lineCred")
        self.gridLayout_2.addWidget(self.lineCred, 0, 1, 1, 1)
        
        
        
        self.lblDbUrl = QtWidgets.QLabel(self.dbGroupBox)
        self.lblDbUrl.setObjectName("lblDbUrl")
        self.gridLayout_2.addWidget(self.lblDbUrl, 1, 0, 1, 1)
        self.lineUrl = QtWidgets.QLineEdit(self.dbGroupBox)
        self.lineUrl.setText("")
        self.lineUrl.setObjectName("lineUrl")
        self.gridLayout_2.addWidget(self.lineUrl, 1, 1, 1, 1)
       
        self.lblDbRef = QtWidgets.QLabel(self.dbGroupBox)
        self.lblDbRef.setObjectName("lblDbRef")
        self.gridLayout_2.addWidget(self.lblDbRef, 2, 0, 1, 1)
        self.lineRef = QtWidgets.QLineEdit(self.dbGroupBox)
        self.lineRef.setText("")
        self.lineRef.setObjectName("lineRef")
        self.gridLayout_2.addWidget(self.lineRef, 2, 1, 1, 1)
         
        self.gridLayout.addWidget(self.dbGroupBox, 1, 0, 1, 2)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 0, 1, 1)
        self.btnSave = QtWidgets.QPushButton(databaseSettings)
        self.btnSave.setObjectName("btnSave")
        self.gridLayout.addWidget(self.btnSave, 0, 1, 1, 1)

        config = configparser.ConfigParser()
        config.read('config.ini')
        self.lineCred.setText(config.get("Database_settings","cred"))
        self.lineUrl.setText(config.get("Database_settings","databaseurl"))
        self.lineRef.setText(config.get("Database_settings","databasereferance"))

        self.lineCred.textChanged.connect(self.dbCred)
        self.lineUrl.textChanged.connect(self.dbUrl)
        self.lineRef.textChanged.connect(self.dbRef)

        
        self.retranslateUi(databaseSettings)
        QtCore.QMetaObject.connectSlotsByName(databaseSettings)

    def retranslateUi(self, databaseSettings):
        _translate = QtCore.QCoreApplication.translate
        databaseSettings.setWindowTitle(_translate("databaseSettings", "Database Settings"))
        self.dbGroupBox.setTitle(_translate("databaseSettings", "Firebase Realtime Database"))
        self.lblCred.setText(_translate("databaseSettings", "Credential:"))
        self.lblDbUrl.setText(_translate("databaseSettings", "Database Url:"))
        self.lblDbRef.setText(_translate("databaseSettings", "Database Referance:"))
        self.btnSave.setText(_translate("databaseSettings", "Save"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    databaseSettings = QtWidgets.QWidget()
    ui = Ui_databaseSettings()
    ui.setupUi(databaseSettings)
    databaseSettings.show()
    sys.exit(app.exec_())
