import pyodbc
from datetime import datetime

class Inventory():

    def __init__(self, wolvoxDb, storage, isAllSync = False):
        self.wolvoxDb  = wolvoxDb
        self.storage   = storage
        self.isAllSync = isAllSync

    def getInventory(self):
        with self.wolvoxDb.cursor() as cursor:
            generateId = 3000
            cursor.execute(self.storedProcedureQuery(generateId))
            cursor.execute(self.getInventoryQuery(generateId) if self.isAllSync else self.getChangedInventoryQuery(generateId))
            data = cursor.fetchall()
            cursor.execute(self.dropTemporaryTable(generateId))
            return data

    def InventoryIdGenerate(self):
        return 'SELECT NEXT VALUE FOR PROG_STOK_MKBAKIYE_GEN'

    def dropTemporaryTable(self, generateId):
        return

    def getChangedInventoryQuery(self, generateId):
        dateFormat = datetime.strptime(self.storage.get('transferLastTime'), "%d.%m.%Y %H:%M:%S")
        dateFormat = dateFormat.strftime('%Y%m%d %H:%M:%S.000')
        return

    def getInventoryQuery(self, generateId):
        return

    def storedProcedureQuery(self, generateId):
        return