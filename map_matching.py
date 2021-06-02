# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MapMatching
                                 A QGIS plugin
 To come
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2021-04-23
        git sha              : $Format:%H$
        copyright            : (C) 2021 by LAEQ
        email                : Philippe.Apparicio@UCS.INRS.ca
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
import os.path
from random import random
import string

from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.core import Qgis, QgsProject, QgsVectorFileWriter
from qgis.PyQt.QtGui import QIcon, QTextCursor
from qgis.PyQt.QtWidgets import QAction , QFileDialog

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .map_matching_dialog import MapMatchingDialog

#Import own class
from .model import imports
from .model.ui.layer_manager import LayerManager
from .model.ui.settings import Settings

from .model.layer import Layers
from .model.network import NetworkLayer
from .model.path import PathLayer
from .model.matcheur import Matcheur


class MapMatching:
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
            'MapMatching_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'q3m.window.title')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None
        self.dlg = None
        self.manager = LayerManager()
        self.layers = None
        self.is_algo_removing = False

        #Test Import:
        self.import_working = imports.check_imports()


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

        return QCoreApplication.translate('MapMatching', message)


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
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/map_matching/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'q3m.toolbar.title'),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""

        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'q3m.window.title'),
                action)
            self.iface.removeToolBarIcon(action)

    def init_ui(self) -> None:
        """ Initialize window with translated messages."""
        
        if self.first_start:
            self.first_start = False
            self.dlg = MapMatchingDialog()
            self.dlg.set_manager(self.manager)

            self.settings = Settings(self.dlg)

            # Translations
            self.dlg.setWindowTitle(self.tr("q3m.window.title"))
            for label, widget in self.dlg.labels():
                label = label.replace("label_", "q3m.window.label.")
                widget.setText(self.tr(label))

            for label, widget in self.dlg.buttons():
                label = label.replace("_", ".").replace("btn", 
                                                        "q3m.window.btn")
                widget.setText(self.tr(label))

            for name, tab in self.dlg.tab():
                label = tab.tabText(0)
                label = label.replace("_", ".").replace("tab", 
                                                        "q3m.window.tab")
                tab.setTabText(0,self.tr(label))

                label = tab.tabText(1)
                label = label.replace("_", ".").replace("tab", 
                                                        "q3m.window.tab")
                tab.setTabText(1,self.tr(label))

            for label, widget in self.dlg.groupBox():
                label = label.replace("_", ".").replace("group", 
                                                        "q3m.window.group")
                widget.setTitle(self.tr(label))

            for label, widget in self.dlg.checkBox():
                if label != "check_speed":
                    label = label.replace("_", ".").replace("check", 
                                                            "q3m.window.check")
                    widget.setText(self.tr(label))

            fixed_elements = []
            fixed_elements.append(self.tr("q3m.window.speed_matching"))
            fixed_elements.append(self.tr("q3m.window.distance_matching"))
            fixed_elements.append(self.tr("q3m.window.closest_matching"))
            self.dlg.fill_fixed_box(fixed_elements)

            #documentation loading
            dir = os.path.dirname(__file__)

            help_name = self.tr("q3m.window.help_file")
            help_settings = self.tr("q3m.window.help_settings_file")

            file = os.path.abspath(os.path.join(dir, './ressources/documentation/', help_name))
            file2 = os.path.abspath(os.path.join(dir,'./ressources/documentation/', help_settings))
            if os.path.exists(file):
                with open(file2) as help2:
                    help = help2.read()
                    self.dlg.textBrowser_settings.insertHtml(help)
                    self.dlg.textBrowser_settings.moveCursor(QTextCursor.Start)

                with open(file) as helpf:
                    help = helpf.read()
                    self.dlg.textBrowser_help.insertHtml(help)
                    self.dlg.textBrowser_help.moveCursor(QTextCursor.Start)
            

            # Listeners
            self.dlg.btn_reload_layers.clicked.connect(self.on_click_reloads)
            
            self.dlg.btn_reduce_network.clicked.connect(self.on_click_reduce_network)
            self.dlg.btn_correct_topology.clicked.connect(self.on_click_correct_topology)
            
            self.dlg.check_speed.clicked.connect(self.dlg.update_matching_box)
            self.dlg.btn_map_matching.clicked.connect(self.on_click_pre_matching)
            
            self.dlg.btn_reselect_path.clicked.connect(self.on_click_reSelect_path)
            self.dlg.btn_apply_path_change.clicked.connect(self.on_click_apply_modification)

            self.dlg.btn_export_matched_track.clicked.connect(self.on_click_export_matched_track)
            self.dlg.btn_export_polyline.clicked.connect(self.on_click_export_polyline)
            self.dlg.btn_export_project.clicked.connect(self.on_click_export_project)

            self.dlg.btn_reset.clicked.connect(self.reset)

            #Temporary=====================================
            self.dlg.dev_tool_import.clicked.connect(self.load)
            #==============================================

            # Prepare the interface buttons
            if not self.import_working:
                #block the interface
                self.error_handler("map_matching.init_ui.import",
                                    level= Qgis.Critical)
                self.dlg.change_button_state(0)
            else:
                #Prepare step 1
                self.dlg.change_button_state(1)

            # Add listener for layer deletion / dragging, ...
            # QgsProject.instance().layerTreeRoot().willRemoveChildren.connect(self.will_removed)
            QgsProject.instance().layerTreeRoot().removedChildren.connect(self.has_removed)
            
        #Setting layer manager and preparing the combobox
        self.manager.set_layers(self.iface.mapCanvas().layers())
        self.dlg.update_layer_box()


    def run(self):
        """Run method that performs all the real work"""
        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        self.init_ui()

        self.dlg.show()
        self.dlg.exec_()


    #def will_removed(self, node, _from, _to) -> None:
        #pass


    #=============================================================================#
    #=========================Interface interaction part==========================#
    #=============================================================================#


    def has_removed(self, node, _from: int, _to: int) -> None:
        """Activate after layer supression, block the plugin to avoid crash."""

        if self.is_algo_removing:
            return

        if self.layers is None:
            self.error_handler(
                    "map_matching.has_removed.pre_algo_layer_deletion",
                    10, Qgis.Info, "Info")
            print("Please reload your comboBox to remove inexistant values")
        else:
            self.error_handler(
                    "map_matching.has_removed.post_algo_layer_deletion",
                    level=Qgis.Critical)
            self.dlg.change_button_state(0)
            """if self.dlg.combo_matched_track.count() == 0:
    
            else:
                self.error_handler("map_matching.has_removed.post_algo_layer_deletion")
                self.dlg.change_button_state(5)
            """


    def on_click_reloads(self):
        """Updates combobox values."""

        self.dlg.clear_combo()
        self.manager.set_layers(self.iface.mapCanvas().layers())
        self.dlg.update_layer_box()


    def load(self):
        """Load sample datas. Usefull for dev-tools."""

        self.is_algo_removing = True
        QgsProject.instance().removeAllMapLayers()
        self.dlg.remove_all_layers()
        self.is_algo_removing = False

        pts_pth = os.path.join(
            self.plugin_dir, "ressources", 
            "datas", "points.gpkg")

        layer = self.iface.addVectorLayer(
            pts_pth, 
            "trace_{:.5f}".format(random()), 
            "ogr")

        self.manager.add_layer(layer)

        network_path = os.path.join(
            self.plugin_dir, "ressources", 
            "datas", "reseau.gpkg")
        
        layer = self.iface.addVectorLayer(
            network_path,
            "reseau_{:.5f}".format(random()),
            "ogr")

        self.manager.add_layer(layer)

        self.dlg.update_layer_box()


    def reset(self):
        """Put back the plugin at the first step."""
        if not self.import_working:
            self.import_working = imports.check_imports()
            if not self.import_working:
                self.error_handler("map_matching.reset.import",
                                    level=Qgis.Critical)
                return

        self.layers = None
        self.dlg.change_button_state(1)
        self.on_click_reloads()
        self.iface.messageBar().clearWidgets()


    #=============================================================================#
    #============================Error handling part==============================#
    #=============================================================================#


    def create_message_error(
            self,
            level : Qgis.MessageLevel,
            message : string,
            pre_message : string = "Error", 
            duration = 10):
        """Create and push a message to QGIS message bar."""

        if duration is None:
            self.iface.messageBar().pushMessage(pre_message,message, level)
        else:
            self.iface.messageBar().pushMessage(
                                    pre_message,message, 
                                    level, duration)
        

    def error_handler(
            self, message: string, 
            duration: int = None, 
            level: Qgis.MessageLevel = Qgis.Warning, 
            pre_message: string = "Error"):
        """Traduce an error and send it to the user.
        
        Format of the message: class.method.class.method... .error
        I.E: map_matching.error_handler.no_message_found
        """

        message_list = message.split('.')
        error_message = message_list[-1].split('-')

        #Traduction of the error
        if error_message[0] == "point_out_of_range":
            #extra information in the output message
            pre_message = "Warning"
            trad = self.tr("q3m.error." + error_message[0])
            pourcentage =  round((int(error_message[1])*100)/int(error_message[2]))
            trad += " " + str(error_message[1]) + " ("+ str(pourcentage) + " %) "
        else:
            #normal case
            trad = self.tr("q3m.error." + message_list[-1])
        
        #creation of the path to the error
        path = " --------------> Path to error: "
        for i in range(len(message_list)-1):
            if i%2 == 0:
                path += message_list[i] + ".py -> "
            else:
                if i == len(message_list)-2:
                    path += message_list[i]
                else:
                    path += message_list[i] + " , "
            
        trad += path
        self.create_message_error(level, trad, pre_message,duration)


    #=============================================================================#
    #==============================Processing part================================#
    #=============================================================================#
    

    def on_click_reduce_network(self) -> None:
        """ Create the object Layers, reduce the network, 
            add the result layer to QGIS."""

        val = self.settings.get_settings()

        #Check input validity
        if val["combo_network"] == "" or val["combo_path"] == "":
            self.error_handler(
                    "map_matching.on_click_reduce_network.missing_input")
            return

        try:
            network_layer = self.manager.find_layer(val["combo_network"])
            path_layer = self.manager.find_layer(val["combo_path"])
        except:
            self.error_handler(
                    "map_matching.on_click_reduce_network.can't_find_layer")
            print("Couldn't find the layer in the combo Box in the list. Please reload the comboBox to remove unexisting layer")
            return
        
        buffer = val["spin_buffer_range"]

        if not LayerManager.are_valid(path_layer, network_layer):
            self.error_handler(
                    "map_matching.on_click_reduce_network.invalid_layer")
            return

        #create the core class
        network_layer = NetworkLayer(network_layer)
        path_layer = PathLayer(path_layer)
        error = path_layer.dupplicate_initial_layer()

        if error is not None:
            #Handle error
            self.error_handler("map_matching.on_click_reduce_network." + error)
            return
        
        self.layers = Layers(path_layer, network_layer)

        #Start the reducing 
        error = self.layers.reduce_network_layer(buffer)

        if error is not None:
            self.error_handler("map_matching.on_click_reduce_network." + error)
            return

        network = self.layers.network_layer.layer

        #applicate change to the application
        self.manager.add_layer(network)

        self.manager.deselect_layer(val["combo_network"])

        self.dlg.change_button_state(2)


    def on_click_correct_topology(self) -> None:
        """Correct the topology of the reduced network then replace it on QGIS."""

        #Check data validity
        if self.layers is None:
            self.error_handler(
                "map_matching.on_click_correct_topology.no_layer")
            return 

        val = self.settings.get_settings()

        #Start the topological correction
        error = self.layers.correct_network_layer_topology( 
            val["spin_close_call"], 
            val["spin_intersection"])

        if error is not None:
            self.error_handler(
                "map_matching.on_click_correct_topology." + error) 
            return

        network = self.layers.network_layer.layer

        #applicate change to the application
        self.manager.add_layer(network)

        self.is_algo_removing = True        #To not trigger has_removed()
        self.manager.remove_layer_from_name("Reduced network")
        
        self.dlg.change_button_state(3)

        self.is_algo_removing = False


    def on_click_pre_matching(self) -> None:
        """Start the process of mapMatching and add the result to QGIS"""
        
        settings = self.settings.get_settings()

        #give a personal ID to every features (some had been duplicated)
        error = self.layers.network_layer.add_attribute_to_layers()

        if error is not None:
            self.error_handler(
                "map_matching.on_click_pre_matching." + error)
            return

        #Create the core class that handle the matching and set it up
        matcheur = Matcheur(self.layers.network_layer.layer, 
                            self.layers.path_layer.layer, 
                            _OID = settings["combo_oid"])
        
        matcheur.set_parameters( settings["spin_searching_radius"],
                                settings["spin_sigma"])

        
        if settings["combo_algo_matching"] == self.tr("q3m.window.speed_matching"):
            res = self.layers.match_speed(
                    matcheur, 
                    settings["combo_speed"], 
                    settings["spin_stop_speed"])

        elif settings["combo_algo_matching"] == self.tr("q3m.window.closest_matching"):
            res = self.layers.match_closest(matcheur)

        elif settings["combo_algo_matching"] == self.tr("q3m.window.distance_matching"):
            res = self.layers.match_by_distance(matcheur)
            
        if res is not None:
            self.error_handler(
                "map_matching.on_click_pre_matching." + res)

        path = self.layers.path_layer.layer

        #applicate change to the application
        self.manager.add_layer(path)

        self.dlg.change_button_state(4)
        self.dlg.update_matched_path_box()


    def on_click_reSelect_path(self) -> None:
        """ Select on the corrected layer the trajectory 
            determined by the last matching algorithm.
        """

        error = self.layers.reSelect_path()

        if error is not None:
            self.error_handler(
                "map_matching.on_click_reSelect_path." + error)
            print("Error in map_matching.reSelect_path")


    def on_click_apply_modification(self) -> None:
        """Create a new matched path layer and add it to QGIS."""
        
        settings = self.settings.get_settings()

        #Create the core class that handle the matching and set it up
        matcheur = Matcheur(
                None, 
                self.layers.path_layer.layer, 
                _OID = settings["combo_oid"])

        matcheur.set_parameters( 
                settings["spin_searching_radius"],
                settings["spin_sigma"])

        #Start the matching after checking the input
        if settings["combo_algo_matching"] == self.tr("q3m.window.speed_matching") :
            error = self.layers.apply_modification( 
                    "speed_matching",
                    matcheur,
                    speed_column_name= settings["combo_speed"],
                    speed_limit = settings["spin_stop_speed"])

            if error is not None:
                self.error_handler(
                    "map_matching.on_click_apply_modification." + error)

        else:
            
            if settings["combo_algo_matching"] == self.tr("q3m.window.distance_matching") :
                type_of_matching = "distance_matching"
            else:
                type_of_matching = "closest_matching"

            error = self.layers.apply_modification( 
                    type_of_matching,
                    matcheur)
            
            if error is not None:
                self.error_handler(
                    "map_matching.on_click_apply_modification." + error)

        path = self.layers.path_layer.layer


        #changing name to avoid confusion on QGIS
        names = []
        for i in range(self.dlg.combo_matched_track.count()):
            names.append(self.dlg.combo_matched_track.itemText(i))

        not_fixed =True
        i = -1
        path_name = ""
        while(not_fixed):
            
            i += 1
            path_name = path.name()

            if i != 0:
                path_name += "_" + str(i)

            not_fixed = False

            for name in names:
                if name == path_name:
                    not_fixed = True
                    break

        path.setName(path_name)

        #applicate change to the application
        self.manager.add_layer(path)
        self.dlg.update_matched_path_box()


    def on_click_export_matched_track(self) -> None:
        """Export the Matched path selected in the comboBox."""

        #Check input validity
        if self.dlg.combo_matched_track.currentText() == "":
            self.error_handler(
                "map_matching.on_click_export_matched_track.no_matched_layer")
            print("Error : no matched layer detected")
            return

        #Get the path to the export folder
        name = QFileDialog.getSaveFileName(
                self.dlg,
                "export : " + self.dlg.combo_matched_track.currentText())
            
        layer = self.manager.find_layer(
                self.dlg.combo_matched_track.currentText())
        
        settings = self.settings.get_settings()

        #Export
        try:
            QgsVectorFileWriter.writeAsVectorFormat(
                layer,name[0],
                "utf-8",
                layer.crs(),
                settings["combo_format"])
        except:
            self.error_handler(
                "map_matching.on_click_export_matched_track.can't_export")

    
    def on_click_export_polyline(self) -> None:
        """Export the polyline of the last matching operation."""

        #Retrieve the polyline from the last matching
        poly = self.layers.get_polyline()
        if isinstance(poly, str):
            self.error_handler(
                "map_matching.on_click_export_polyline." + poly)
            print("Error in export project, couldn't create the polyline")
            return
        settings = self.settings.get_settings()
    
        #Get the path to the export folder
        name = QFileDialog.getSaveFileName(self.dlg,"Save polyline as: ")

        #Export
        try:
            QgsVectorFileWriter.writeAsVectorFormat(
                    poly, name[0], 
                    "utf-8", poly.crs(),
                    settings["combo_format"])
        except:
            self.error_handler(
                "map_matching.on_click_export_polyline.can't_export")


    def on_click_export_project(self) -> None:
        """Export every element of the project checked in settings."""

        settings = self.settings.get_settings()

        #verify the checked box in the settings then add the corresponding ones
        exported_layers = []
        
        if settings["check_initial_path"]:
            exported_layers.append(
                self.layers.path_layer.initial_layer)

        if settings["check_polyline"]:
            poly = self.layers.get_polyline()
            if isinstance(poly, str):
                self.error_handler(
                    "map_matching.on_click_export_project." + poly)
                print("Error in export project, couldn't create the polyline")
                return
            exported_layers.append(poly)

        if settings["check_corrected_network"]:
            exported_layers.append(
                self.layers.network_layer.layer)

        if settings["check_matched_path"]:
            layers = self.manager.get_matched_layers()
            if len(layers) == 0:
                self.error_handler(
                    "map_matching.on_click_export_project.no_matched_layer")
                print("Error in export project: No matched layer found")
            for layer in layers:
                exported_layers.append(layer)
            
        if(len(exported_layers) == 0):
            self.error_handler(
                "map_matching.on_click_export_project.nothing_to_export")
            print("Error : nothing to export. See the export settings and check the boxes that interest you")
            return

        #bug to correct
        if len(exported_layers)>1 and settings["combo_format"] == "ESRI Shapefile":
            print("There is a problem with exporting the project as shapefile")
            return

        #Get the path to the export folder
        name = QFileDialog.getSaveFileName(
            self.dlg,"export : " + self.dlg.combo_matched_track.currentText())

        #Export
        try:
            #setup the export
            options = QgsVectorFileWriter.SaveVectorOptions()
            options.driverName = settings["combo_format"]
            options.layerName = exported_layers[0].name()
            context = QgsProject.instance().transformContext()

            #create file and write one layer inside
            QgsVectorFileWriter.writeAsVectorFormatV2(
                exported_layers[0], name[0],
                context, options)

            #Change option to append news vector to the file
            options.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteLayer

            for i in range(1,len(exported_layers)):
                options.layerName = exported_layers[i].name()
                QgsVectorFileWriter.writeAsVectorFormatV2(
                    exported_layers[i],
                    name[0],
                    context,options)
        
        except:
            self.error_handler(
                "map_matching.on_click_export_project.can't_export")

