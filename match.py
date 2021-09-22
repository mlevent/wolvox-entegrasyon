from PyQt5 import QtCore, QtGui, QtWidgets, uic
from nodetree import NodeTree

from category import Category

class Match(QtWidgets.QDialog):
    def __init__(self, **kwargs):
        super(Match, self).__init__()
        uic.loadUi('./commons/ui/category.ui', self)
        self.setWindowIcon(QtGui.QIcon('./commons/ui/assets/favicon.svg'))
        self.initApp(**kwargs)
    
    def initApp(self, **kwargs):
        self.localDb  = kwargs['localDb']
        self.wolvoxDb = kwargs['wolvoxDb']
        self.remoteDb = kwargs['remoteDb']

        category = Category(self.localDb, self.wolvoxDb, self.remoteDb)
        remoteCategoryNodes = category.getCategoryNodes(True)

        for localId, localItem in category.getCategoryNodes().items():
            combo = QtWidgets.QComboBox()
            combo.setMaxVisibleItems(50)
            combo.wheelEvent = lambda event: None
            combo.addItem('< LÜTFEN SEÇİNİZ >', None)
            for remoteId, remoteName in remoteCategoryNodes.items():
                combo.addItem(remoteName, remoteId)
            
            findSelect = combo.findData(localItem['matchId'])
            combo.setCurrentIndex(findSelect)
            if findSelect:
                combo.setStyleSheet("font-weight:bold; color:green;")

            #combo.activated[str].connect(self.comboActivate) # 2) How would I go about accessing the QComboBoxes
            combo.activated.connect(
                lambda state, localId=localId: self.comboActivate(state, localId)
            )
            self.MatchForm.addRow(QtWidgets.QLabel(localItem['name']), combo)

    def comboActivate(self, selectIndex, localId):
        combo = self.sender()
        matchId = combo.itemData(selectIndex)
        cursor = self.localDb.cursor()
        cursor.execute('UPDATE wvcategories SET matchId = ? WHERE id = ?', [matchId, localId])
        self.localDb.commit()