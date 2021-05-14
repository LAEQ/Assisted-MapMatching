from qgis import processing
from qgis.core import *
from qgis.PyQt.QtCore import QVariant

# from .topology import *
from shapely import wkt

from .utils.layerTraductor import *

from .topology import *
from .utils.geometry import connect_lines

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


    def select_intersection_trajectory(self, buffer) -> QgsVectorLayer:
        """Reduce the network layer features by only keeping the line intersecting the buffer

        Input:
        buffer -- A buffer of type QgsVectorLayer

        """

        # Sécurité: on commence à vide
        self.initial_layer.removeSelection()

        test = processing.run("qgis:selectbylocation",
                              {'INPUT': self.initial_layer, 'PREDICATE': 0, 'INTERSECT': buffer, 'METHOD': 0})

        reduced_layer = self.initial_layer.materialize(
            QgsFeatureRequest().setFilterFids(self.initial_layer.selectedFeatureIds()))
        self.initial_layer.removeSelection()

        #Deselect the precedent network
        #QgsProject.instance().layerTreeRoot().findLayer(self.initial_layer.id()).setItemVisibilityChecked(False)

        
        reduced_layer.setName("Reduced network")
        self.layer = reduced_layer


        #QgsProject.instance().addMapLayer(self.reduced_layer)


    def correct_topology(self, close_call_tol, inter_dangle_tol):
        """Correct the topology of the layer."""

        shapely_dict = layerTraductor.from_vector_layer_to_list_of_dict(self.layer)

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


    def add_attribute_to_layers(self, attribute_name = 'joID'):
        """ Create a new column to the network_layer indexed from 0 to the number of feature in the layer  

        Input:
        attribute_name : -- A string that represent the name of the new column
        """

        #self.layer = self.initial_layer

        provider = self.layer.dataProvider()

        provider.addAttributes([QgsField(attribute_name,QVariant.Int)])

        self.layer.updateFields()

        test = len(self.layer.fields().names())-1

        self.layer.startEditing()
        i=0
        for f in self.layer.getFeatures():
            tesid = f.id()
            attr_value={test:i}
            provider.changeAttributeValues({tesid:attr_value})
            i+=1
        self.layer.commitChanges()


    def find_path(self, matcheur): 
        """Find a possible route 
        
        Input: 
        matcheur :  -- An object of class Matcheur 
        """
        
        matcheur.find_best_path_in_network()

        self.possible_path = matcheur.tag_id

        self.select_possible_path()

    
    def select_possible_path(self):
        """ Select in the network_layer the path recorded at the last matching """

        if(self.possible_path) == None:
            print("error : path not created yet")
            return -1

        self.layer.selectByExpression('"joID" in (' +','.join(self.possible_path)+ ')' )


    def change_possible_path(self): #penser à mettre un warning si layer vide de selection
        """ Change the path recorded """

        self.possible_path = [str(feat['joID']) for feat in self.layer.getSelectedFeatures()]

    def create_vector_from_path(self):
        """Create a QgsVectorLayer from the selected features """

        layer = processing.run("native:saveselectedfeatures", {'INPUT': self.layer, 'OUTPUT': 'memory:'})['OUTPUT']
        layer.setName("path for matching")

        return layer

    def concatenate_line(self,layer,oid_column_name):
        l = layerTraductor.from_vector_layer_to_list_of_dict(layer)
        l = layerTraductor.order_list_of_dict(l,oid_column_name)

        new_list = []

        start = False

        index = 0

        for i in range (len(l)-1):
            if l[i][oid_column_name] == l[i+1][oid_column_name]:
                if(start == False):
                    index = i
                start = True
            else:
                if start == True:
                    new_feat = l[index]


                    for j in range (index,i+1): #+1

                        new_feat["geometry"] = connect_lines(new_feat["geometry"],l[j]["geometry"])

                    new_list.append(new_feat)
                    start = False

                else:
                    print(l[i]["fid"])
                    new_list.append(l[i])

        if start == True:
            new_feat = l[index]

            for j in range (index+1,len(l)): #+1
                new_feat["geometry"] = connect_lines(new_feat,l[j]["geometry"])

            start = False
            new_list.append(new_feat)
        else:
            new_list.append(l[-1])

        return layerTraductor.from_list_of_dict_to_layer(new_list,self.layer)