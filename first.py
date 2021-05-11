# -*- coding: utf-8 -*-
"""
/***************************************************************************
 first
                                 A QGIS plugin
 Premier plugin test
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2021-04-03
        git sha              : $Format:%H$
        copyright            : (C) 2021 by jojo
        email                : test@gmail.com
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
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication , Qt
from qgis.PyQt.QtGui import QIcon, QTextCursor
from qgis.PyQt.QtWidgets import QAction, QPushButton, QProgressBar, QPushButton, QCheckBox
from qgis.core import *
import copy

from .layerTraductor import *
import random


# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .first_dialog import firstDialog
import os.path

#import personnal class
from .layers import *
from .worker import *

class first:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'first_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        #==================================================================================

        #AJOUT 
        self.dlg = firstDialog()

        #add help-document to the GUI
        dir = os.path.dirname(__file__)
        file = os.path.abspath(os.path.join(dir, '.', 'help.html'))
        file2 = os.path.abspath(os.path.join(dir,'.', 'help_settings.html'))
        if os.path.exists(file):
            with open(file2) as help2:
                help = help2.read()
                self.dlg.textBrowser_settings.insertHtml(help)
                self.dlg.textBrowser_settings.moveCursor(QTextCursor.Start)

            with open(file) as helpf:
                help = helpf.read()
                self.dlg.textBrowser_help.insertHtml(help)
                self.dlg.textBrowser_help.moveCursor(QTextCursor.Start)


                

        

        #AJOUT PERSO: connection boutton penser à en faire une fonction ?
        self.dlg.pushButtonExportLine.clicked.connect(self.load_element)
        self.dlg.pushButtonReloadLayers.clicked.connect(self.fill_comboBox)

        self.dlg.pushButtonReduceNetwork.clicked.connect(self.reduce_network_layer)
        self.dlg.pushButtonCorrectTopology.clicked.connect(self.correct_topology)
        self.dlg.pushButtonMapMatching.clicked.connect(self.start_mapMatching)
        self.dlg.pushButtonReselectPath.clicked.connect(self.on_click_reSelect_path)
        self.dlg.pushButtonApplyPathChange.clicked.connect(self.on_click_apply_modification)
        self.dlg.pushButtonReset.clicked.connect(self.reset) 

        #self.dlg.pushButtonMapMatching.setEnabled(True)
        #self.dlg.pushButtonCorrectTopology.setEnabled(True)

        self.dlg.comboBoxAlgoMatching.addItem("Matching with Speed")
        self.dlg.comboBoxAlgoMatching.addItem("Matching closest")
        self.dlg.comboBoxAlgoMatching.addItem("Matching by distance")
        

        #change attributes elements when path layer comboBox is activated
        self.dlg.comboBoxPathLayer.activated.connect(self.fill_attribute_comboBox)

        self.layers = None
        #buggé à garder en mémoire
        #root = QgsProject.instance().layerTreeRoot()
        #root.visibilityChanged.connect(self.info)

        #==================================================================================


        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&first')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

        """ ligne 82: mise à jour comboBox quand selection de layer
            def info(self,layerTreeNode):
        self.fill_comboBox()
        print("info" + layerTreeNode.name())"""


    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('first', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToVectorMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/first/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'TEST'),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True

        #AJOUT
    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""

        for action in self.actions:
            self.iface.removePluginVectorMenu(
                self.tr(u'&first'),
                action)
            self.iface.removeToolBarIcon(action)


    def run(self):
        """Run method that performs all the real work"""

        self.fill_comboBox(False)

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start == True:
            self.first_start = False

            

        # show the dialog
        self.dlg.show()
        # Run the dialog event loop

    #==============================================================================================================================
    #                                       Mon code
    #==============================================================================================================================


    #===============================================================================#
    #===========================Threading part======================================#
    #===============================================================================#

    #phase test: plusieurs bugs: bug selection layer, Penser à voir si implémentable dans layers
    def startWorker(self, layers, work_to_do):
        """Start and set up a thread to do heavy work in background, workerFinished will be trigger after the thread end
        
        Input:
        layers     -- An object of class Layers
        work_to_do -- A string representing the work to be done
                      3 possible values for now: reduce_network_layer, 
                                                 correct_topology,
                                                 matching
        """
        
        self.disable_all_buttons()

        # create a new worker instance
        worker = Worker(layers)

        # configure the QgsMessageBar
        messageBar = self.iface.messageBar().createMessage('Heavy work in the background: ' + work_to_do, )
        progressBar = QProgressBar()
        progressBar.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        
        cancelButton = QPushButton()
        cancelButton.setText('Cancel')
        cancelButton.clicked.connect(worker.kill)

        messageBar.layout().addWidget(progressBar)
        messageBar.layout().addWidget(cancelButton)
        self.iface.messageBar().pushWidget(messageBar, Qgis.Info)
        self.messageBar = messageBar

        # start the worker in a new thread
        thread = QtCore.QThread(worker)
        worker.moveToThread(thread)
        worker.finished.connect(self.workerFinished)
        worker.error.connect(self.workerError)
        worker.progress.connect(progressBar.setValue)

        if(work_to_do == "reduce_network_layer"):
            worker.add_range(self.dlg.spinBoxBufferRange.value())
            thread.started.connect(worker.run_reduce_network_layer)
        elif(work_to_do == "correct_topology"):
            thread.started.connect(worker.run_correct_topology)
        elif(work_to_do == "matching"):
            thread.started.connect(worker.run_map_matching)

        thread.start()
        self.thread = thread
        self.worker = worker

    def workerFinished(self, ret):
        """Start once a thread from startWorker is finished: Clean the thread and apply the result."""

        

        # clean up the worker and thread
        self.thread.quit()
        self.thread.wait()
        self.thread.deleteLater()
        self.worker.deleteLater()
        # remove widget from message bar

        self.iface.messageBar().popWidget(self.messageBar)
        if ret is not None:
            # report the result

            work_to_do = ret
            
            self.iface.messageBar().pushMessage("work done, " + work_to_do)

            if(work_to_do == "reduce_network_layer"):
                QgsProject.instance().addMapLayer(self.layers.network_layer.layer)
                self.dlg.pushButtonCorrectTopology.setEnabled(True)

            elif(work_to_do == "correct_topology" ):
                QgsProject.instance().addMapLayer(self.layers.network_layer.layer)
                self.dlg.pushButtonMapMatching.setEnabled(True)

            elif(work_to_do == "matching"):
                self.dlg.pushButtonReselectPath.setEnabled(True)

        else:
            # notify the user that something went wrong
            self.iface.messageBar().pushMessage('Something went wrong! See the message log for more information.', level=Qgis.Critical, duration=3)
        
        print("end thread")
    

    def workerError(self, e, exception_string):
        print("Error: " + 'Worker thread raised an exception: ')
        print("------------------------------------------------------ \n")
        print(exception_string)
        print("------------------------------------------------------")
        #QgsMessageLog.logMessage('Worker thread raised an exception:\n'.format(exception_string), level=Qgis.Critical)


    #===============================================================================#
    #===========================action function part================================#
    #===============================================================================#


    def reduce_network_layer(self):
        if self.__create_layers_class()!= -1 :
            #self.startWorker(self.layers,"reduce_network_layer")

            settings = self.recup_settings()

            self.layers.reduce_network_layer(settings["spinBoxBufferRange"])

            QgsProject.instance().addMapLayer(self.layers.network_layer.layer)

            self.dlg.pushButtonCorrectTopology.setEnabled(True)
            self.dlg.pushButtonReduceNetwork.setEnabled(False)


    def correct_topology(self):
        if self.__create_layers_class() != -1:
            #self.startWorker(self.layers,"correct_topology")

            settings = self.recup_settings()

            if settings["checkBox_Speed"] :
                self.layers.reduce_Path_layer(settings["comboBoxSpeed"], settings["spinBoxStopSpeed"])
            self.layers.correct_network_layer_topology(settings["spinBoxCloseCall"],settings["spinBoxIntersection"])
            self.dlg.pushButtonMapMatching.setEnabled(True)
            self.dlg.pushButtonCorrectTopology.setEnabled(False)


    def start_mapMatching(self): 

        if self.__create_layers_class() != -1:
            #self.startWorker(self.layers,"matching")

            settings = self.recup_settings()

            #we prepare the network layer
            self.layers.network_layer.add_attribute_to_layers()

            #We create the matching class
            matching = mapMatching(self.layers.network_layer.layer,self.layers.path_layer.layer, _OID= settings["comboBoxOID"])
            matching.setParameters(settings["spinBoxSearchingRadius"], settings["spinBoxSigma"])

            #We call the matching function
            if settings["comboBoxAlgoMatching"] == "Matching with Speed":
                if(settings["checkBox_Speed"] == False):
                    print("error")
                    return

                self.layers.reduce_Path_layer(settings["comboBoxSpeed"],settings["spinBoxStopSpeed"])
                self.layers.match_speed(matching, settings["comboBoxSpeed"])

            elif settings["comboBoxAlgoMatching"] == "Matching closest":
                self.layers.match_closest(matching)

            elif settings["comboBoxAlgoMatching"] == "Matching by distance":
                self.layers.match_by_distance(matching)

            self.dlg.pushButtonMapMatching.setEnabled(False)
            self.dlg.pushButtonReselectPath.setEnabled(True)
            self.dlg.pushButtonApplyPathChange.setEnabled(True)


    def on_click_reSelect_path(self):
        self.layers.reSelect_path()


    def on_click_apply_modification(self):
        
        settings = self.recup_settings()

        if settings["comboBoxAlgoMatching"] == "Matching with Speed" :
            if settings["checkBox_Speed"] == False:
                print("error speed not checked and use speed matching")
                return

            self.layers.reduce_Path_layer(  settings["comboBoxSpeed"],
                                            settings["spinBoxStopSpeed"])

            self.layers.apply_modification( settings["comboBoxAlgoMatching"], 
                                            search_rad = settings["spinBoxSearchingRadius"],
                                            sigma = settings["spinBoxSigma"],
                                            speed_column_name= settings["comboBoxSpeed"], 
                                            OID=  settings["comboBoxOID"])

        else:
            self.layers.apply_modification(settings["comboBoxAlgoMatching"],
                                                    search_rad = settings["spinBoxSearchingRadius"],
                                                    sigma = settings["spinBoxSigma"],
                                                    OID= settings["comboBoxOID"])

        

        


    #===============================================================================#
    #===========================layer utility part==================================#
    #===============================================================================#


    def __create_layers_class(self):
        if(self.layers != None):
            return 0

        settings = self.recup_settings()

        network_layer = self.get_layer(settings["comboBoxNetworkLayer"])
        path_layer = self.get_layer(settings["comboBoxPathLayer"])

        if not self.__check_layer_validity(network_layer,path_layer):
            return -1

        self.layers = Layers(path_layer,network_layer)
        return 1

    

    def __check_layer_validity(self,network_layer,path_layer):
        """Verify if the two layers respect the specification.


        Input:
        network_layer -- A QgsVectorLayer
        path_layer    -- A QgsVectorLayer

        Output:
        True  -- The 2 layers has the same projection system and use a cartesian system
        False -- Every other configuration
        """

        if(network_layer == None):

            self.create_message_error("No network layer detected, makes sure the layer is active in the layer tab  : Refresh?",
                                      "Refresh",
                                      Qgis.Critical)
            return False

        if(path_layer == None):
            self.create_message_error("No Path layer detected, makes sure the layer is active in the layer tab : Refresh?",
                                      "Refresh",
                                      Qgis.Critical)
            return False


        #We check the Distance Unit of the projection system: 0 = DistanceMeters, 6 = DistanceDegrees...
        if(network_layer.crs().mapUnits()!=0):
            self.iface.messageBar().pushMessage("Error", 'Error the Network layer doesn\'t use a cartesian projection system',level=Qgis.Critical)
            return False
        if(path_layer.crs().mapUnits()!=0):
            self.iface.messageBar().pushMessage("Error", 'Error the Path layer doesn\'t use a cartesian projection system',level=Qgis.Critical)
            return False

        #We check if the two layers use the same projection system
        if(network_layer.crs().authid() != path_layer.crs().authid()):
            self.iface.messageBar().pushMessage('Error the two selected layers'
                                                +'has different projection system')
            return False

        return True


    def get_layer(self, layer_name):
        """Return the QgsVectorLayer with the name layer_name."""

        layers = self.iface.mapCanvas().layers()

        for layer in layers:
            if layer.name() == layer_name:
                return layer
        return None

    #===============================================================================#
    #================================GUI part=======================================#
    #===============================================================================#

    def disable_all_buttons(self):
        self.dlg.pushButtonReduceNetwork.setEnabled(False)
        self.dlg.pushButtonCorrectTopology.setEnabled(False)
        self.dlg.pushButtonMapMatching.setEnabled(False)
        self.dlg.pushButtonReselectPath.setEnabled(False)     
        self.dlg.pushButtonApplyPathChange.setEnabled(False)


    def create_message_error(self,message,button_message,level):
        widget = self.iface.messageBar().createMessage("Error",message)
        button = QPushButton(widget)
        button.setText(button_message)
        button.pressed.connect(self.fill_comboBox)
        widget.layout().addWidget(button)
        self.iface.messageBar().pushWidget(widget, level = level)

    #Remplissage des comboBox
        
    def fill_comboBox(self, clear_message = True):
        """Fill the 3 comboBox (2 layers and 2 attributes) according to 
            the value present in the layer tab.
        """

        if(clear_message):
            self.iface.messageBar().clearWidgets()

        #get all layers in the current QGIS project
        layers = self.iface.mapCanvas().layers()

        #fill the comboBox
        cb1 = self.fill_layer_comboBox(layers, self.dlg.comboBoxNetworkLayer, 'LINESTRING')
        cb2 = self.fill_layer_comboBox(layers, self.dlg.comboBoxPathLayer, 'POINT')

        if(cb1 != 0 and cb2 != 0 ):
            self.dlg.pushButtonReduceNetwork.setEnabled(True)
        else:
            self.dlg.pushButtonReduceNetwork.setEnabled(False)

        self.fill_attribute_comboBox()

        
    def fill_layer_comboBox(self, layers, comboBox, geom_type):
        """Fill the layers comboBox.


        Input:
        layers   --  A list of layers
        comboBox --  A QComboBox 
        geom_type -- A String
        """

        #first clear the comboBox
        comboBox.clear()

        i=0
        #populate the comboBox
        for layer in layers:
            #ignore raster layer, because just vector layers have a wkbType
            if layer.type() == 0:
                if (QgsWkbTypes.flatType(layer.wkbType()) == QgsWkbTypes.Point and geom_type == 'POINT' or 
                    QgsWkbTypes.flatType(layer.wkbType()) == QgsWkbTypes.LineString and geom_type == 'LINESTRING'):

                    comboBox.addItem(layer.name())
                    i+=1

        return i

    def empty_oid_comboBox(self):
        self.dlg.comboBoxOID.clear()
        self.empty_oid_comboBox = True

    def empty_speed_comboBox(self):
        self.dlg.comboBoxSpeed.clear()
        self.empty__comboBox


    def fill_attribute_comboBox(self):
        """Fill the attribute comboBox."""

        #clear the comboBox
        self.dlg.comboBoxOID.clear()
        self.dlg.comboBoxSpeed.clear()

        #get the selected Path layer in the comboBox
        layer = self.get_layer(self.dlg.comboBoxPathLayer.currentText())

        #No layer activated
        if(layer==None):
            #self.iface.messageBar().pushMessage('Error no layer charged in qgis')
            return

        for field in layer.fields():
            if (field.typeName()=="Integer" or 
                field.typeName()=="Integer64" or
                field.typeName()=="int8" or 
                field.typeName()=="integer"):
                    self.dlg.comboBoxOID.addItem(field.name())
            elif (field.typeName() == "Real" or
                  field.typeName()=="double"):
                    self.dlg.comboBoxSpeed.addItem(field.name())


    #===============================================================================#
    #=============Code Perso pour faciliter le dev==================================#
    #===============================================================================#


    #Fonction temporaire et personnel
    #charge un exemple en un clique dans qgis: pour faciliter le developpement
    def load_element(self):

        QgsProject.instance().removeAllMapLayers()


        layer = self.iface.addVectorLayer("/Users/jordy/OneDrive/Documents/Cours/Stage Montreal/Import QGIS/trajetV4_reprojeté.shp", "", "ogr")
        if not layer:
            print("Layer failed to load!")
        layer.setName("Path layer: V4")

        layer = self.iface.addVectorLayer("/Users/jordy/OneDrive/Documents/Cours/Stage Montreal/Import QGIS/mapParis.gpkg", "", "ogr")
        if not layer:
            print("Layer failed to load!")
        layer.setName("Map de Paris")

        for layer in QgsProject.instance().mapLayers().values():
            if(layer.name() != "Path layer: V4" and layer.name() != "Map de Paris"):
                print(type(layer))
                node = QgsProject.instance().layerTreeRoot().findLayer(layer)
                if node:
                    node.setItemVisibilityChecked(False)

        print(layer.sourceName())

        self.fill_comboBox(False)


    #Fonction temporaire pour faciliter les tests sans avoir à passer par de nombreuses fonctions
    def reset(self):
        #reset
        print("func")
        self.disable_all_buttons()
        self.dlg.pushButtonReduceNetwork.setEnabled(True)
        self.layers = None

    def test(self):
        self.layers.network_layer.add_attribute_to_layers()
        matching = mapMatching(self.layers.network_layer.layer,self.layers.path_layer.layer, _OID= self.dlg.comboBoxOID.currentText())
        matching.find_best_path_in_network()
        self.layers.network_layer.possible_path = matching.tag_id
        self.layers.reSelect_path()

    def recup_settings(self):
        dico = {}

        dico["comboBoxNetworkLayer"] = self.dlg.comboBoxNetworkLayer.currentText()
        dico["comboBoxPathLayer"] = self.dlg.comboBoxPathLayer.currentText()

        dico["spinBoxBufferRange"] = self.dlg.spinBoxBufferRange.value()

        dico["checkBox_Speed"] = self.dlg.checkBox_Speed.isChecked()
        dico["spinBoxStopSpeed"] = self.dlg.spinBoxStopSpeed.value()
        dico["comboBoxSpeed"] = self.dlg.comboBoxSpeed.currentText()

        dico["spinBoxCloseCall"] = self.dlg.spinBoxCloseCall.value()
        dico["spinBoxIntersection"] = self.dlg.spinBoxIntersection.value()

        dico["spinBoxSearchingRadius"] = self.dlg.spinBoxSearchingRadius.value()
        dico["spinBoxSigma"] = self.dlg.spinBoxSigma.value()

        dico["comboBoxOID"] = self.dlg.comboBoxOID.currentText()

        dico["comboBoxAlgoMatching"] = self.dlg.comboBoxAlgoMatching.currentText()


        return dico

        
        



