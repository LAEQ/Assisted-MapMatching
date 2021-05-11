class Settings:

    def __init__(self,_dlg):
        self.dlg = _dlg
        self.dictionnary = {}

    def update(self):

        self.dictionnary = {}
        self.dictionnary["comboBoxNetworkLayer"] = self.dlg.comboBoxNetworkLayer.currentText()
        self.dictionnary["comboBoxPathLayer"] = self.dlg.comboBoxPathLayer.currentText()

        self.dictionnary["spinBoxBufferRange"] = self.dlg.spinBoxBufferRange.value()

        self.dictionnary["checkBox_Speed"] = self.dlg.checkBox_Speed.isChecked()
        self.dictionnary["spinBoxStopSpeed"] = self.dlg.spinBoxStopSpeed.value()
        self.dictionnary["comboBoxSpeed"] = self.dlg.comboBoxSpeed.currentText()

        self.dictionnary["spinBoxCloseCall"] = self.dlg.spinBoxCloseCall.value()
        self.dictionnary["spinBoxIntersection"] = self.dlg.spinBoxIntersection.value()

        self.dictionnary["spinBoxSearchingRadius"] = self.dlg.spinBoxSearchingRadius.value()
        self.dictionnary["spinBoxSigma"] = self.dlg.spinBoxSigma.value()

        self.dictionnary["comboBoxOID"] = self.dlg.comboBoxOID.currentText()

        self.dictionnary["comboBoxAlgoMatching"] = self.dlg.comboBoxAlgoMatching.currentText()
    
    def get_dict(self):
        self.update()
        return self.dictionnary

