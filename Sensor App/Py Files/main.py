import firebase_admin
import pytemperature
import threading
import time
import datetime
import sys
import os
import base64
import codecs
import json
"""import paho.mqtt.client as mqtt"""
import binascii
import win32api
import configparser
import requests
import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from firebase_admin import credentials
from firebase_admin import db
from PyQt5 import QtCore, QtGui, QtWidgets
from binascii import hexlify
from io import BytesIO
from requests.exceptions import HTTPError
from threading import Thread
from urllib.request import urlopen
from PyQt5 import QtCore, QtGui, QtWidgets
from settingsWindow import Ui_SensorSettings
from dbSettingsWindow import Ui_databaseSettings
import webbrowser
from listPrinter import Window
class Ui_MainWindow(object):
    def openPrint(self):
        app = QtWidgets.QApplication(sys.argv)
        window = Window(self)        
        window.show()        
        window.show()    
    def closeEvent(self):
        win32api.MessageBox(0,f'Are you sure to quit?','Quit Request',0x00000020)
    def saveItems(self):    
        try:
            savedTime=time.strftime('%H.%M.%S, %d-%m-%Y')
            list_Text = self.listWidget
            textFile = '\n'.join(list_Text.item(ii).text() for ii in range (list_Text.count()))
            with open(f"Sensor Values - {savedTime}.txt","w") as output:
                output.write(textFile)
            win32api.MessageBox(0,f'List Widget items saved in application path successfully!','Info',0x00000040)
        except Exception as e:
            win32api.MessageBox(0,f'Error Message: {e}','An error occured!',0x00000010)      
    def aboutLink(self):
        win32api.MessageBox(0,f'It is an application to control used sensors and its data information.\n\n' +
            'For get more information about Sensor Application please contact with developer.\n\n' +
                'Tayfun GÜVEN - Mail: tayfun.guven25@gmail.com  \n', 'ABOUT',0x00000020)               
    def helpLink(self):
        new=2
        url="--"
        webbrowser.open(url, new=new) 
    #connection of settingsWindow.py (SENSOR SETTINGS)
    def openSensorSettings(self):
        self.settings =  QtWidgets.QWidget()
        self.ui = Ui_SensorSettings()
        self.ui.setupUi(self.settings)
        self.settings.show()    
    def openDatabaseSettings(self):
        self.dbSettings = QtWidgets.QWidget()
        self.ui = Ui_databaseSettings()
        self.ui.setupUi(self.dbSettings)
        self.dbSettings.show()
    def loadDataToFirebase(self):       
        #bunları db settings oluşturup configDb ye at
        ##########################
        ####################
        def background():            
            while True:        
                config = configparser.ConfigParser()
                config.read('config.ini')
                api_address = config.get('Sensor_settings','sensor1Source')                           
                url = api_address
                json_data = requests.get(url).json()
                formatted_data = json_data['temperature']
                formatted_data2 = formatted_data + 33.78
                starttime=time.time()
                ts=time.time()
                st=datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S %d-%m-%Y')#('%Y-%m-%d %H:%M:%S')
                """xxx = config.get('Database_settings','databasereferance')
                ref = db.reference(xxx)"""
                ref = db.reference(config.get('Database_settings','databaseReferance'))                
                
                
                try:                        
                    data={'temp':formatted_data,'hum':formatted_data2,'ts':int(ts),'dt':st}
                    ref.push(data)
                    time.sleep(5.0-(time.time()-starttime)%5.0)
                    
                except Exception as e:
                    #win32api.MessageBox(0,f'An error occured: \n{e}', 'Program has stopped working!',0x00000010) 
                    print (e)
                    time.sleep(50)
                
           
        a = threading.Thread(name='background',target=background)
        a.start()
    def showFirebaseData(self):
        def listWidgetData():
            while True:
                config = configparser.ConfigParser()
                config.read('config.ini')
                starttime=time.time()
                #ref = db.reference('test')  
                ref = db.reference(config.get('Database_settings','databaseReferance')) 
                try:
                    jsons = ref.order_by_child('ts').get()        
                    q = []
                    for json in jsons: 
                        #self.listWidget.addItem(("Temperature: " + str(jsons[json]['temp']) + "°C" + "     Date: " + str(jsons[json]['dt'])))
                        q.append(("Temperature: " + str(jsons[json]['temp']) + "°C" + "     Humidity: "+ str(jsons[json]['hum'])  + "     Date: " + str(jsons[json]['dt'])))
                        #enqueue
                        if len (q)>=6:
                            q.pop(0)
                        #dequeue
                        self.listWidget.clear()
                        self.listWidget.addItem('\n'.join(map(str, q)))
                        
                    #print ("Temperature: " + str(jsons[json]['temp']) + "°C" + "     Date: " + str(jsons[json]['dt']))
                    time.sleep(5.0-(time.time()-starttime)%5.0)
                except Exception as e:
                    win32api.MessageBox(0,f'an error occured: \n{e}', 'Program has stopped working!',0x00000010)  
                    time.sleep(10)
        b = threading.Thread(name='listWidgetData', target=listWidgetData)
        b.start()  
    
    def setupUi(self, MainWindow):
        
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(701, 350)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("temperatureIcon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.dataArea = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(50)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dataArea.sizePolicy().hasHeightForWidth())
        self.dataArea.setSizePolicy(sizePolicy)
        self.dataArea.setObjectName("dataArea")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.dataArea)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.btnRunData = QtWidgets.QPushButton(self.dataArea)
        self.btnRunData.setObjectName("btnRunData")
        self.gridLayout_2.addWidget(self.btnRunData, 1, 0, 1, 1)
        self.btnRunData.clicked.connect(self.loadDataToFirebase)
        self.listWidget = QtWidgets.QListWidget(self.dataArea)
        self.listWidget.setObjectName("listWidget")
        self.gridLayout_2.addWidget(self.listWidget, 0, 0, 1, 4)
        self.btnShowData = QtWidgets.QPushButton(self.dataArea)
        self.btnShowData.setObjectName("btnShowData")
        self.gridLayout_2.addWidget(self.btnShowData, 1, 1, 1, 1)
        self.btnShowData.clicked.connect(self.showFirebaseData)
        self.btnClear = QtWidgets.QPushButton(self.dataArea)
        self.btnClear.setObjectName("btnClear")
        self.gridLayout_2.addWidget(self.btnClear, 1, 2, 1, 1)
        self.btnStop = QtWidgets.QPushButton(self.dataArea)
        self.btnStop.setObjectName("btnStop")
        self.gridLayout_2.addWidget(self.btnStop, 1, 3, 1, 1)
        self.gridLayout_5.addWidget(self.dataArea, 0, 1, 1, 1)
        self.sensorArea = QtWidgets.QScrollArea(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sensorArea.sizePolicy().hasHeightForWidth())
        self.sensorArea.setSizePolicy(sizePolicy)
        self.sensorArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.sensorArea.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.sensorArea.setWidgetResizable(True)
        self.sensorArea.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.sensorArea.setObjectName("sensorArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 336, 289))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBoxSensor1 = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(100)
        sizePolicy.setVerticalStretch(10)
        sizePolicy.setHeightForWidth(self.groupBoxSensor1.sizePolicy().hasHeightForWidth())
        self.groupBoxSensor1.setSizePolicy(sizePolicy)
        self.groupBoxSensor1.setObjectName("groupBoxSensor1")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBoxSensor1)
        self.gridLayout.setVerticalSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.labelHum = QtWidgets.QLabel(self.groupBoxSensor1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelHum.sizePolicy().hasHeightForWidth())
        self.labelHum.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.labelHum.setFont(font)
        self.labelHum.setObjectName("labelHum")
        self.gridLayout.addWidget(self.labelHum, 1, 0, 1, 1)
        self.lcdHum = QtWidgets.QLCDNumber(self.groupBoxSensor1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lcdHum.sizePolicy().hasHeightForWidth())
        self.lcdHum.setSizePolicy(sizePolicy)
        self.lcdHum.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.lcdHum.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.lcdHum.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcdHum.setObjectName("lcdHum")
        self.gridLayout.addWidget(self.lcdHum, 1, 1, 1, 1)
        self.labelTemp = QtWidgets.QLabel(self.groupBoxSensor1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelTemp.sizePolicy().hasHeightForWidth())
        self.labelTemp.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.labelTemp.setFont(font)
        self.labelTemp.setObjectName("labelTemp")
        self.gridLayout.addWidget(self.labelTemp, 0, 0, 1, 1)
        self.lcdTemp = QtWidgets.QLCDNumber(self.groupBoxSensor1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lcdTemp.sizePolicy().hasHeightForWidth())
        self.lcdTemp.setSizePolicy(sizePolicy)
        self.lcdTemp.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.lcdTemp.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.lcdTemp.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcdTemp.setObjectName("lcdTemp")
        self.gridLayout.addWidget(self.lcdTemp, 0, 1, 1, 1)
        self.labelC = QtWidgets.QLabel(self.groupBoxSensor1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelC.sizePolicy().hasHeightForWidth())
        self.labelC.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.labelC.setFont(font)
        self.labelC.setObjectName("labelC")
        self.gridLayout.addWidget(self.labelC, 0, 2, 1, 1)
        self.labelRh = QtWidgets.QLabel(self.groupBoxSensor1)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.labelRh.setFont(font)
        self.labelRh.setObjectName("labelRh")
        self.gridLayout.addWidget(self.labelRh, 1, 2, 1, 1)
        self.verticalLayout.addWidget(self.groupBoxSensor1, 0, QtCore.Qt.AlignVCenter)
        self.groupBoxSensor2 = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(100)
        sizePolicy.setVerticalStretch(10)
        sizePolicy.setHeightForWidth(self.groupBoxSensor2.sizePolicy().hasHeightForWidth())
        self.groupBoxSensor2.setSizePolicy(sizePolicy)
        self.groupBoxSensor2.setObjectName("groupBoxSensor2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBoxSensor2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.labelTemp2 = QtWidgets.QLabel(self.groupBoxSensor2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelTemp2.sizePolicy().hasHeightForWidth())
        self.labelTemp2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.labelTemp2.setFont(font)
        self.labelTemp2.setObjectName("labelTemp2")
        self.gridLayout_3.addWidget(self.labelTemp2, 0, 0, 1, 1)
        self.lcdTemp2 = QtWidgets.QLCDNumber(self.groupBoxSensor2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lcdTemp2.sizePolicy().hasHeightForWidth())
        self.lcdTemp2.setSizePolicy(sizePolicy)
        self.lcdTemp2.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.lcdTemp2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.lcdTemp2.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcdTemp2.setObjectName("lcdTemp2")
        self.gridLayout_3.addWidget(self.lcdTemp2, 0, 1, 1, 1)
        self.labelC2 = QtWidgets.QLabel(self.groupBoxSensor2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelC2.sizePolicy().hasHeightForWidth())
        self.labelC2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.labelC2.setFont(font)
        self.labelC2.setObjectName("labelC2")
        self.gridLayout_3.addWidget(self.labelC2, 0, 2, 1, 1)
        self.verticalLayout.addWidget(self.groupBoxSensor2, 0, QtCore.Qt.AlignVCenter)
        self.groupBoxSensor3 = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(100)
        sizePolicy.setVerticalStretch(10)
        sizePolicy.setHeightForWidth(self.groupBoxSensor3.sizePolicy().hasHeightForWidth())
        self.groupBoxSensor3.setSizePolicy(sizePolicy)
        self.groupBoxSensor3.setObjectName("groupBoxSensor3")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBoxSensor3)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.statusBar = QtWidgets.QProgressBar(self.groupBoxSensor3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statusBar.sizePolicy().hasHeightForWidth())
        self.statusBar.setSizePolicy(sizePolicy)
        self.statusBar.setProperty("value", 100)
        self.statusBar.setTextVisible(False)
        self.statusBar.setFormat("")
        self.statusBar.setObjectName("statusBar")
        self.gridLayout_4.addWidget(self.statusBar, 0, 3, 1, 1)
        self.labelAMode = QtWidgets.QLabel(self.groupBoxSensor3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelAMode.sizePolicy().hasHeightForWidth())
        self.labelAMode.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.labelAMode.setFont(font)
        self.labelAMode.setObjectName("labelAMode")
        self.gridLayout_4.addWidget(self.labelAMode, 0, 0, 1, 1)
        self.lcdAMode = QtWidgets.QLCDNumber(self.groupBoxSensor3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lcdAMode.sizePolicy().hasHeightForWidth())
        self.lcdAMode.setSizePolicy(sizePolicy)
        self.lcdAMode.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.lcdAMode.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.lcdAMode.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcdAMode.setObjectName("lcdAMode")
        self.gridLayout_4.addWidget(self.lcdAMode, 0, 1, 1, 1)
        self.labelStatus = QtWidgets.QLabel(self.groupBoxSensor3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelStatus.sizePolicy().hasHeightForWidth())
        self.labelStatus.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelStatus.setFont(font)
        self.labelStatus.setObjectName("labelStatus")
        self.gridLayout_4.addWidget(self.labelStatus, 0, 2, 1, 1)
        self.verticalLayout.addWidget(self.groupBoxSensor3)
        self.sensorArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_5.addWidget(self.sensorArea, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 701, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuSettings = QtWidgets.QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionSave_as = QtWidgets.QAction(MainWindow)
        self.actionSave_as.setObjectName("actionSave_as")
        
        
        
        

        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionPrint = QtWidgets.QAction(MainWindow)
        self.actionPrint.setObjectName("actionPrint")
        self.actionView = QtWidgets.QAction(MainWindow)
        self.actionView.setObjectName("actionView")
        self.actionSensorSettings = QtWidgets.QAction(MainWindow)
        self.actionSensorSettings.setObjectName("actionSensorSettings")
        self.actionQuit.triggered.connect(self.closeEvent)
        """self.btnRunData.clicked.connect(self.newObject)"""
        self.btnClear.clicked.connect(self.listWidget.clear)
        ########
        self.actionSensorSettings.triggered.connect(self.openSensorSettings)
        self.actionDatabaseSettings = QtWidgets.QAction(MainWindow)
        self.actionDatabaseSettings.setObjectName("actionDatabaseSettings")
        self.actionDatabaseSettings.triggered.connect(self.openDatabaseSettings)
        self.actionHelp = QtWidgets.QAction(MainWindow)
        self.actionHelp.setObjectName("actionHelp")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionPrint)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuSettings.addAction(self.actionView)
        self.menuSettings.addSeparator()
        self.menuSettings.addAction(self.actionSensorSettings)
        self.menuSettings.addSeparator()
        self.menuSettings.addAction(self.actionDatabaseSettings)
        self.menuHelp.addAction(self.actionHelp)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        def lcdDataSensor1(): 
            #renklerde sıkıntı var açıldığında program duruyor
            #self.groupBoxDevices.setTitle("Device 1")
            while True:
                try:                    
                    #self.groupBoxSensor1.setTitle("Sensor 1")
                    config = configparser.ConfigParser()
                    config.read('config.ini')
                    api_address = config.get('Sensor_settings','sensor1Source')
                    sensType = config.get('Sensor_settings','sensor1Type')
                    #activStatue = config.get('Sensor_rules','sensor1Statue')
                    url = api_address                    
                    json_data = requests.get(url).json()
                    
                        
                    if sensType == 'Temperature - Humidity':
                        self.lcdHum.setEnabled(True)
                        self.labelHum.setEnabled(True)
                        self.labelRh.setEnabled(True)
                        self.lcdHum.setVisible(True)
                        self.labelHum.setVisible(True)
                        self.labelRh.setVisible(True)
                        formatted_data = json_data['temperature']
                        formatted_data2 = formatted_data + 33.78
                        formatted_data3 = json_data['epoch']
                        """formatted_data = pytemperature.k2c(json_data['temperature'])
                        formatted_data2 = json_data['humidity']
                        formatted_data3 = json_data['epoch']"""
                        epochTime = formatted_data3
                        controlTime = int(time.time())
                        diff = controlTime - epochTime
                        try:
                            if diff>=10:
                                self.groupBoxSensor1.setTitle("Sensor 1 - Last seen: {}".format(epochTime))
                                #self.groupBoxSensor1.setStyleSheet("QGroupBox:title { color: red }")

                            else:
                                self.groupBoxSensor1.setTitle("Sensor 1 - Time: {}".format(epochTime))
                                #self.groupBoxSensor1.setStyleSheet("QGroupBox:title { color: default }")
                        except Exception as x:
                            win32api.MessageBox(0,f'An error occured! \n {x}','Error occured',0x00000010)
                        data = float(formatted_data)
                        data2 = float(formatted_data2)
                        #temperature
                        if data > float(config.get('Sensor_settings','sensor1TMaxValue')):
                            self.lcdTemp.display(data) 
                            win32api.MessageBox(0,'Extreme High Temperature!', 'WARNING!',0x00000030)
                            """self.lcdTemp.setStyleSheet("QLCDNumber { background-color: white }") 
                            time.sleep(1)                          
                            self.lcdTemp.setStyleSheet("QLCDNumber { background-color: red }")
                            time.sleep(1)"""
                        elif data < float (config.get('Sensor_settings','sensor1TMinValue')):
                            self.lcdTemp.display(data) 
                            win32api.MessageBox(0,'Extreme Low Temperature!', 'WARNING!',0x00000030)
                            """self.lcdTemp.setStyleSheet("QLCDNumber { background-color: white }") 
                            time.sleep(1)                          
                            self.lcdTemp.setStyleSheet("QLCDNumber { background-color: blue }")
                            time.sleep(1)"""
                        else:
                            self.lcdTemp.display(data) 
                        
                        #humidity
                        if data2 > float(config.get('Sensor_settings','sensor1HMaxValue')):
                            self.lcdHum.display(data2)
                            win32api.MessageBox(0,'Extreme High Humidity!', 'WARNING!',0x00000030) 
                            """self.lcdHum.setStyleSheet("QLCDNumber { background-color: white }") 
                            time.sleep(1)                          
                            self.lcdHum.setStyleSheet("QLCDNumber { background-color: red }")
                            time.sleep(1)"""
                                    
                        elif data2 < float(config.get('Sensor_settings','sensor1HMinValue')):
                            self.lcdHum.display(data2)
                            win32api.MessageBox(0,'Extreme Low Humidity!', 'WARNING',0x00000030)
                            """self.lcdHum.setStyleSheet("QLCDNumber { background-color: white }") 
                            time.sleep(1)                          
                            self.lcdHum.setStyleSheet("QLCDNumber { background-color: blue }")
                            time.sleep(1)"""
                        else:
                            self.lcdHum.display(data2)  
                                
                        time.sleep(10)  
                    elif sensType == 'Temperature':
                        self.lcdHum.setEnabled(False)
                        self.labelHum.setEnabled(False)
                        self.labelRh.setEnabled(False)
                        self.lcdHum.setVisible(False)
                        self.labelHum.setVisible(False)
                        self.labelRh.setVisible(False)
                        formatted_data = json_data['temperature']                        
                        formatted_data3 = json_data['epoch']
                        epochTime = formatted_data3
                        controlTime = int(time.time())
                        diff = controlTime - epochTime
                        try:
                            if diff>=10:
                                self.groupBoxSensor1.setTitle("Sensor 1 - Last seen: {}".format(epochTime))
                                #self.groupBoxSensor1.setStyleSheet("QGroupBox:title { color: red }")
                            else:
                                self.groupBoxSensor1.setTitle("Sensor 1 - Time: {}".format(epochTime))
                                #self.groupBoxSensor1.setStyleSheet("QGroupBox:title { color: default }")
                        except Exception as x:
                            win32api.MessageBox(0,f'An error occured! \n {x}','Error occured',0x00000010)
                        data = float(formatted_data)
                        #temperature
                        if data > float(config.get('Sensor_settings','sensor1TMaxValue')):
                            self.lcdTemp.display(data) 
                            win32api.MessageBox(0,'Extreme High Temperature!', 'WARNING!',0x00000030)
                            """self.lcdTemp.setStyleSheet("QLCDNumber { background-color: white }") 
                            time.sleep(1)                          
                            self.lcdTemp.setStyleSheet("QLCDNumber { background-color: red }")
                            time.sleep(1)"""
                        elif data < float (config.get('Sensor_settings','sensor1TMinValue')):
                            self.lcdTemp.display(data) 
                            win32api.MessageBox(0,'Extreme Low Temperature!', 'WARNING!',0x00000030)
                            """self.lcdTemp.setStyleSheet("QLCDNumber { background-color: white }") 
                            time.sleep(1)                          
                            self.lcdTemp.setStyleSheet("QLCDNumber { background-color: blue }")
                            time.sleep(1)"""
                        else:
                            self.lcdTemp.display(data)        
                        time.sleep(10)

                    else:
                        print ("its light sensor!")
                        
                    """else:
                        config.set('Sensor_rules','sensor1statue','0')
                        self.lcdTemp.display("000")
                        win32api.MessageBox(0,'Please check sensor settings!', 'Information',0x00000020 )
                        time.sleep(10)"""
                except Exception as e:
                    ts=time.time()
                    st=datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S %d-%m-%Y')
                    self.groupBoxSensor1.setTitle("Sensor 1 - Last seen: {}".format(st))
                    win32api.MessageBox(0,f'An error occured: \n{e} \n\nSensor 1 - Last seen: {st}','Program has stopped working!',0x00000010)
                    time.sleep(10)
        c=threading.Thread(name='lcdDataSensor1',target=lcdDataSensor1)
        c.start()
        """self.btnStop.clicked.connect(self.stopThreads)"""
        self.actionPrint.triggered.connect(self.openPrint)
        self.actionSave.triggered.connect(self.saveItems)
        self.actionHelp.triggered.connect(self.helpLink)
        
        self.actionAbout.triggered.connect(self.aboutLink)
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Sensor Application"))
        self.dataArea.setTitle(_translate("MainWindow", "Data Screen"))
        self.btnRunData.setText(_translate("MainWindow", "Run Database"))
        self.btnShowData.setText(_translate("MainWindow", "Show Data"))
        self.btnClear.setText(_translate("MainWindow", "Clear"))
        self.btnStop.setText(_translate("MainWindow", "Stop"))
        self.groupBoxSensor1.setTitle(_translate("MainWindow", "Sensor 1"))
        self.labelHum.setText(_translate("MainWindow", "Humidity:"))
        self.labelTemp.setText(_translate("MainWindow", "Temp:"))
        self.labelC.setText(_translate("MainWindow", "°C"))
        self.labelRh.setText(_translate("MainWindow", "%rh"))
        self.groupBoxSensor2.setTitle(_translate("MainWindow", "Sensor 2"))
        self.labelTemp2.setText(_translate("MainWindow", "Temp:    "))
        self.labelC2.setText(_translate("MainWindow", "°C"))
        self.groupBoxSensor3.setTitle(_translate("MainWindow", "Sensor 3"))
        self.labelAMode.setText(_translate("MainWindow", "Alert Mode:"))
        self.labelStatus.setText(_translate("MainWindow", "Status:"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuSettings.setTitle(_translate("MainWindow", "Settings"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionSave.setText(_translate("MainWindow", "Save as .txt"))
        self.actionSave_as.setText(_translate("MainWindow", "Save as..."))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionPrint.setText(_translate("MainWindow", "Print"))
        self.actionView.setText(_translate("MainWindow", "View"))
        self.actionSensorSettings.setText(_translate("MainWindow", "Sensor Settings"))
        self.actionDatabaseSettings.setText(_translate("MainWindow", "Database Settings"))
        self.actionHelp.setText(_translate("MainWindow", "Help"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        
        

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    config = configparser.ConfigParser()
    config.read('config.ini')
    cred = credentials.Certificate(config.get("Database_settings","cred"))
    firebase_admin.initialize_app(cred,{
        'databaseURL':(config.get("Database_settings","databaseurl"))
    })
    sys.exit(app.exec_())
