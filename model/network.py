from qgis import processing
from qgis.core import *
from qgis.PyQt.QtCore import QVariant

from .utils.layerTraductor import *

from .topology import *


"""
This class take care of the network layer
It has 2 objects:
It's initial layer: layer
The reduced one : reduced_layer
"""


class NetworkLayer:

    def __init__(self, _layer):
        self.initial_layer = _layer
        self.layer = self.initial_layer


    def select_intersection_trajectory(self, buffer):
        """Reduce the network layer features by only keeping the line intersecting the buffer

        Input:
        buffer -- A buffer of type QgsVectorLayer

        """

        # Sécurité: on commence à vide
        self.initial_layer.removeSelection()
        try:
            test = processing.run("qgis:selectbylocation",
                            {'INPUT': self.initial_layer, 'PREDICATE': 0, 'INTERSECT': buffer, 'METHOD': 0})
        except:
            print("Error processing in select_intersection_trajectory (Network.py)")
            return "network.select_intersection_trajectory.processing"

        reduced_layer = self.initial_layer.materialize(
            QgsFeatureRequest().setFilterFids(self.initial_layer.selectedFeatureIds()))
        self.initial_layer.removeSelection()

        reduced_layer.setProviderEncoding("UTF-8")

        #Deselect the precedent network
        #QgsProject.instance().layerTreeRoot().findLayer(self.initial_layer.id()).setItemVisibilityChecked(False)

        
        reduced_layer.setName("Reduced network")
        self.layer = reduced_layer


        #QgsProject.instance().addMapLayer(self.reduced_layer)


    def correct_topology(self, close_call_tol, inter_dangle_tol):
        """Correct the topology of the layer."""

        shapely_dict = layerTraductor.from_vector_layer_to_list_of_dict(self.layer)

        if type(shapely_dict) == str:
            return "network.correct_topology." + shapely_dict

        # We truncate all the points value
        corrected_list = simplify_coordinates(shapely_dict, 3)

        # We split the loops  (i.e: roundabouts)
        corrected_list = cut_loops(corrected_list)

        # We take care of the intersection
        corrected_list = deal_with_danglenodes(corrected_list, inter_dangle_tol)
        corrected_list = deal_with_intersections(corrected_list, inter_dangle_tol)

        # We connect roads wich extremities are close to each other
        corrected_list = deal_with_closecall(corrected_list, close_call_tol)

        self.layer = layerTraductor.from_list_of_dict_to_layer(corrected_list, self.layer, "LineString", "corrected layer")
        
        if type(self.layer) == str:
            return "network.correct_topology." + self.layer

    def add_attribute_to_layers(self, attribute_name = 'joID'):
        """ Create a new column to the network_layer indexed from 0 to the number of feature in the layer  

        Input:
        attribute_name : -- A string that represent the name of the new column
        """

        if attribute_name == "" or attribute_name == None:
            return "network.add_attribute_to_layers.empty_attribute_name"

        provider = self.layer.dataProvider()

        provider.addAttributes([QgsField(attribute_name,QVariant.Int)])

        self.layer.updateFields()

        length = len(self.layer.fields().names())-1

        self.layer.startEditing()
        i=0
        for f in self.layer.getFeatures():
            tesid = f.id()
            attr_value={length:i}
            provider.changeAttributeValues({tesid:attr_value})
            i+=1
        self.layer.commitChanges()


    def find_path(self, matcheur): 
        """Find a possible route 
        
        Input: 
        matcheur :  -- An object of class Matcheur 
        """
        
        result = matcheur.find_best_path_in_network()

        if type(result) == str:
            return "network.find_path."+result

        self.possible_path = matcheur.tag_id

        self.select_possible_path()

    
    def select_possible_path(self):
        """ Select in the network_layer the path recorded at the last matching """

        if(self.possible_path) == None:
            #print("error : path not created yet") "network.select_possible_path.no_path.registered"
            return "network.select_possible_path.no_path_registered"
        try:
            self.layer.selectByExpression('"joID" in (' +','.join(self.possible_path)+ ')' )
        except:
            print("Seems like the network has been deleted")

    def change_possible_path(self): #penser à mettre un warning si layer vide de selection
        """ Change the path recorded """
        
        if self.layer.selectedFeatureCount() <=0:
            print("Nothing has been selected: potential problem. Please select a road at least")
            return "network.change_possible_path.no_selection"

        self.possible_path = [str(feat['joID']) for feat in self.layer.getSelectedFeatures()]

    def create_vector_from_path(self) -> QgsVectorLayer:
        """Create a QgsVectorLayer from the selected features """

        layer = processing.run("native:saveselectedfeatures", {'INPUT': self.layer, 'OUTPUT': 'memory:'})['OUTPUT']
        layer.setName("path for matching")

        return layer