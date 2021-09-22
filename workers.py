import time
import math
import requests
import hashlib
import base64
import pymysql
import pyodbc
import xmltodict

from PyQt5 import QtCore, QtWidgets

from inventory import Inventory
from remote import Remote
from generate import Generate
from category import Category

'''
' ENVANTER LİSTESİ İSTEĞİ
'''
class GetInventoryThread(QtCore.QThread):
    
    listenInventory = QtCore.pyqtSignal(dict)
    finishInventory = QtCore.pyqtSignal(dict)

    def __init__(self, localDb, wolvoxDb, remoteDb, settings, storage, isAllSync):
        QtCore.QThread.__init__(self)
        self.localDb   = localDb
        self.wolvoxDb  = wolvoxDb
        self.remoteDb  = remoteDb
        self.settings  = settings
        self.storage   = storage
        self.isAllSync = isAllSync
        self.isRunning = True

    def run(self):

        try:
            self.inventory   = Inventory(self.wolvoxDb, self.storage, self.isAllSync)
            self.remote      = Remote(self.remoteDb)
            self.localCursor = self.localDb.cursor()

            # Güncellemeyi Başlat
            self.remote.updateStart()

            inventoryList = self.inventory.getInventory()
            if isinstance(inventoryList, list):
                inventoryCount = len(inventoryList)
                if inventoryCount > 0:
                    loopInventory = 0
                    saveInventory = 0    
                    for inventoryItem in inventoryList:
                        
                        # İşlem Durdurulduysa
                        if not self.isRunning:
                            self.finishInventory.emit({'success': True, 'total': 0, 'saveTotal': 0})
                            break
                        
                        # Ürünü İşleme Gönder
                        if inventoryItem:
                            
                            try:
                                saveItem = self.remote.updateRemote(inventoryItem, self.getCategoryMatchId(inventoryItem))
                            except:
                                continue

                    # Eşitleme Tamamlandı
                    if self.isRunning:
                        if saveInventory and self.isAllSync:
                            self.remote.updateStatus()
                        self.finishInventory.emit({'success': True, 'total': inventoryCount, 'saveTotal': saveInventory})

                # Envanter Listesi Boşsa
                else:
                    self.finishInventory.emit({'success': True, 'total': 0, 'saveTotal': 0})
            
            # Envanter Listesinde Hata Varsa
            else:
                self.finishInventory.emit({'success': False})

        # Aktarımda Hata Oluşursa
        except:
            self.finishInventory.emit({'success': False})

    def getCategoryMatchId(self, item):
        if item.ALT_GRUBU and item.ALT_GRUBU is not None and item.ARA_GRUBU is not None and item.GRUBU is not None:
            ctree = '/'.join([item.GRUBU, item.ARA_GRUBU, item.ALT_GRUBU])
        elif item.ARA_GRUBU and item.ARA_GRUBU is not None and item.GRUBU is not None:
            ctree = '/'.join([item.GRUBU, item.ARA_GRUBU])
        elif item.GRUBU and item.GRUBU is not None:
            ctree = item.GRUBU
        else:
            ctree = None

    def stop(self):
        self.isRunning = False
        self.quit()

'''
' ENVANTER LİSTESİ İSTEĞİ
'''
class GetCategoryThread(QtCore.QThread):
    
    listenCategory = QtCore.pyqtSignal(int)
    finishCategory = QtCore.pyqtSignal(int)

    def run(self):
        self.listenCategory.emit(1)
        category = Category(self.localDb, self.wolvoxDb, self.remoteDb)
        category.getCategorySync()
        self.finishCategory.emit(1)

'''
' WOLVOX BAĞLANTI İSTEĞİ
'''
class WolvoxConnectThread(QtCore.QThread):
    
    listenWolvox = QtCore.pyqtSignal(int)
    finishWolvox = QtCore.pyqtSignal(dict)

    def __init__(self, settings):
        QtCore.QThread.__init__(self)
        self.settings = settings

    def run(self):
        self.listenWolvox.emit(1)
        try:
            con = pyodbc.connect(dsn)
            con.timeout = 15
            self.finishWolvox.emit({'success': True, 'db': con})
        except:
            self.finishWolvox.emit({'success': False})

'''
' REMOTE BAĞLANTI İSTEĞİ
'''
class RemoteConnectThread(QtCore.QThread):
    
    listenRemote = QtCore.pyqtSignal(int)
    finishRemote = QtCore.pyqtSignal(dict)

    def __init__(self, settings):
        QtCore.QThread.__init__(self)
        self.settings = settings

    def run(self):
        self.listenRemote.emit(1)
        try:
            self.finishRemote.emit({'success': True, 'db': con})
        except:
            self.finishRemote.emit({'success': False})

'''
' WOLVOX SDK BAĞLANTI İSTEĞİ
'''
class SdkConnectThread(QtCore.QThread):
    
    listenSdk = QtCore.pyqtSignal(int)
    finishSdk = QtCore.pyqtSignal(dict)

    def __init__(self, settings):
        QtCore.QThread.__init__(self)
        self.settings = settings

    def run(self):

        self.listenSdk.emit(1)

        sqlPass = hashlib.md5(self.settings['wolvoxSqlPass'].encode()).hexdigest()
        
        loginQuery = str('command=wlogin&username={}&password={}&devCode={}&devPass={}').format(self.settings['wolvoxSqlUser'], sqlPass, self.settings['wolvoxDevUser'], self.settings['wolvoxDevPass'])
        loginQuery = base64.b64encode(loginQuery.encode())


'''
' WOLVOX SDK SİPARİŞLERİ İÇE AKTAR
'''
class SdkOrderThread(QtCore.QThread):
    
    listenOrder = QtCore.pyqtSignal(dict)
    finishOrder = QtCore.pyqtSignal(dict)

    def __init__(self, remoteDb, settings, storage):
        QtCore.QThread.__init__(self)
        self.remoteDb = remoteDb
        self.settings = settings
        self.storage  = storage

    def run(self):

        try:
            remote = Remote(self.remoteDb)
            orders = remote.getOrders()

            if orders is not None:
                for order in orders:

                    try:
                        
                        invRequest = requests.get('http://%s:%s/getdata.html?%s' % (self.settings['wolvoxIp'], self.settings['wolvoxPort'], base64.b64encode(invQuery.encode()).decode()))

                        if invRequest.status_code == 200:
                            response = base64.b64decode(invRequest.content).decode()
                            status, info = response.split('^')
                            if status == 'XML_POST_OK':
                                invId, invCode = info.replace('MBLKODU=', '').split(',')
                                remote.updateOrder(order['id'], invId, invCode)
                                self.listenOrder.emit({'message': '%s numaralı fatura işlendi...' % (invCode)})
                            else:
                                self.listenOrder.emit({'message': info})
                    except:
                        continue

            self.finishOrder.emit({'success': True})

        except:
            self.finishOrder.emit({'success': False})