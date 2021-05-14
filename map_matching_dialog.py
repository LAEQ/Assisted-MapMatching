# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MapMatchingDialog
                                 A QGIS plugin
 To come
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2021-04-23
        git sha              : $Format:%H$
        copyright            : (C) 2021 by LAEQ
        email                : Philippe.Apparicio@UCS.INRS.Ca
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os
from qgis.PyQt import uic
from qgis.PyQt import QtWidgets
from qgis.PyQt.QtWidgets import QLabel, QPushButton, QComboBox, QTabWidget, QGroupBox, QCheckBox
from qgis.core import QgsVectorLayer, QgsFields
from typing import List
from .model.ui.button_manager import Button_manager

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
# from model.layer_manager import LayerManager
# from .model.layer_manager import LayerManager

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'map_matching_dialog_base.ui'))


class MapMatchingDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(MapMatchingDialog, self).__init__(parent)
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

        self.manager = None
        self.buttonManager = Button_manager(self)
        self.fill_fixed_box()

        """Listeners"""
        self.combo_path.currentIndexChanged.connect(self.on_path_changed)

    def set_manager(self, manager) -> None:
        self.manager = manager
        paths = self.manager.path_layers()
        self.combo_path.addItems([path.name() for path in paths])
        networks = self.manager.network_layers()
        self.combo_network.addItems([network.name() for network in networks])

    #def set_buttons_manager(self, but_manager) -> None:
        #self.buttonManger = Button_manager(self)

    def update(self):
        self.save_selected()
        self.clear()
        paths = self.manager.path_layers()
        self.combo_path.addItems([path.name() for path in paths])
        networks = self.manager.network_layers()
        self.combo_network.addItems([network.name() for network in networks])
        
        self.reselect_saved()
        self.update_matched_path_box()
        

    def save_selected(self):
        network = self.combo_network.currentText()
        path = self.combo_path.currentText()
        OID = self.combo_oid.currentText()
        speed = self.combo_speed.currentText()
        self.manager.save(path,network,OID,speed)

    def reselect_saved(self):
        print(self.manager.selected_path)
        if  self.manager.selected_path != "" and self.manager.selected_path != self.combo_path.currentText():
            self.combo_path.setCurrentIndex(self.combo_path.findText(self.manager.selected_path))
        if  self.manager.selected_path != "" and self.manager.selected_network != self.combo_network.currentText():
            self.combo_network.setCurrentIndex(self.combo_network.findText(self.manager.selected_network))
        if  self.manager.OID != "" and self.manager.OID != self.combo_oid.currentText():
            self.combo_oid.setCurrentIndex(self.combo_oid.findText(self.manager.OID))
        if  self.manager.speed != "" and self.manager.speed != self.combo_speed.currentText():
            self.combo_speed.setCurrentIndex(self.combo_speed.findText(self.manager.speed))


    def clear(self):
        self.combo_path.clear()
        self.combo_network.clear()
        self.combo_oid.clear()
        self.combo_speed.clear()

    def add_path(self, layer: QgsVectorLayer):
        self.combo_path.addItem(layer.name())

    def add_network(self, layer: QgsVectorLayer):
        self.combo_network.addItem(layer.name())

    def remove_layer(self, layer) -> None:
        pass
    
    def remove_all_layers(self) -> None:
        self.manager.set_layers([])
        self.clear()
        
    def change_button_state(self, state: int):
        """Change the buttons state
        
        Input:
        state -- The state of the plugin: 
                0 = Everything locked
                1 = Input phase
                2 = Correcting phase
                3 = Matching phase
                4 = Modification phase
                5 = Import phase
        """
        if self.buttonManager == None:
            print("Error: no button manager created")
            return -1

        if state == 0 :
            self.buttonManager.disable_all_buttons()
        elif state == 1:
            self.buttonManager.set_input_state_buttons()
        elif state == 2:
            self.buttonManager.set_topology_state_buttons()
        elif state == 3: 
            self.buttonManager.set_pre_matching_state_buttons()
        elif state == 4:
            self.buttonManager.set_modification_state_buttons()
        elif state == 5:
            self.buttonManager.set_import_state()

    def fill_fixed_box(self):
        self.combo_algo_matching.addItem("Matching with Speed")
        self.combo_algo_matching.addItem("Matching closest")
        self.combo_algo_matching.addItem("Matching by distance")
        self.combo_format.addItem("GPKG")
        self.combo_format.addItem("ESRI Shapefile")

    def update_matching_box(self):
        if self.check_speed.isChecked():
            self.combo_algo_matching.addItem("Matching with Speed")
            index = self.combo_algo_matching.findText("Matching with Speed")
            self.combo_algo_matching.setCurrentIndex(index)
        else:
            index = self.combo_algo_matching.findText("Matching with Speed")
            self.combo_algo_matching.removeItem(index)

            index = self.combo_algo_matching.findText("Matching by distance")
            self.combo_algo_matching.setCurrentIndex(index)
    
    def update_matched_path_box(self):
        self.combo_matched_track.clear()
        layers = self.manager.matched_layers()
        self.combo_matched_track.addItems([layer.name() for layer in layers])


    """Listeners"""
    def on_path_changed(self):
        self.combo_oid.clear()
        self.combo_speed.clear()

        index = self.combo_path.currentIndex()
        fields = self.manager.path_attributes(index)
        self.combo_oid.addItems([field.name() for field in fields if (  field.typeName() == "Integer" or 
                                                                        field.typeName()=="Integer64" or
                                                                        field.typeName()=="int8" or 
                                                                        field.typeName()=="integer")])
        self.combo_speed.addItems([field.name() for field in fields if (  field.typeName() == "Real" or 
                                                                            field.typeName()=="double")])

    def __iter__(self):
        for attr, value in self.__dict__.iteritems():
            yield attr, value

    """Getters"""
    def labels(self):
        return filter(lambda elem: isinstance(elem[1], QLabel), self.__dict__.items())

    def buttons(self):
        return filter(lambda elem: isinstance(elem[1], QPushButton), self.__dict__.items())

    def tab(self):
        return filter(lambda elem: isinstance(elem[1], QTabWidget), self.__dict__.items())

    def groupBox(self):
        return filter(lambda elem: isinstance(elem[1], QGroupBox), self.__dict__.items())
    
    def checkBox(self):
        return filter(lambda elem: isinstance(elem[1], QCheckBox), self.__dict__.items())