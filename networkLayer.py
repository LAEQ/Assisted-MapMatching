from qgis import processing
from qgis.core import *
from qgis.PyQt.QtCore import QVariant

from .topology import *
from shapely import wkt

"""
This class take care of the network layer
It has 2 objects:
It's initial layer: layer
The reduced one : reduced_layer

"""

class NetworkLayer:


    def __init__(self, _layer):
        self.initial_layer = _layer


    def select_intersection_trajectory(self,buffer):
        """Reduce the network layer features by only keeping the line intersecting the buffer

        Input:
        buffer -- A buffer of type QgsVectorLayer

        """

        #Sécurité: on commence à vide
        self.initial_layer.removeSelection()

        test = processing.run("qgis:selectbylocation", {'INPUT': self.initial_layer, 'PREDICATE': 0, 'INTERSECT' : buffer , 'METHOD' : 0})
        
        self.reduced_layer = self.initial_layer.materialize(QgsFeatureRequest().setFilterFids(self.initial_layer.selectedFeatureIds()))
        self.initial_layer.removeSelection()

        #Temporary line to show the progression
        QgsProject.instance().addMapLayer(self.reduced_layer)
        print("Reduced layer: ")
        

    def correct_topology(self):
        """Correct the topology of the layer."""

        
        shapely_dict = self.__from_vector_layer_to_list_of_dict(self.reduced_layer)

        #We truncate all the points value 
        corrected_list = simplify_coordinates(shapely_dict,3)

        #We split the loops  (i.e: roundabouts)
        corrected_list = cut_loops(corrected_list)

        #We take care of the intersection
        corrected_list = deal_with_danglenodes(corrected_list)
        corrected_list = deal_with_intersections(corrected_list)

        #We connect roads wich extremities are close to each other
        corrected_list = deal_with_closecall(corrected_list)


        self.reduced_layer = self.__from_list_of_dict_to_layer(corrected_list)

        #Temporary line : Ajout de la couche à l'application
        QgsProject.instance().addMapLayer(self.reduced_layer)


    def __from_vector_layer_to_list_of_dict(self,layer):
        """Transform the input layer into a format readable for shapely

        Input:
        layer -- A QgsVectorLayer

        Output:
        final_list -- A list composed of the dictionnary version of each feature plus a pair ['geometry']
        i.e: 
        final_list = [ 
            {'fid': 1 , 'speed': 3.14 , 'geometry' : wktGeometry}, 
            { 'fid': 2 , ...}, 
            ... 
        ]
 
        """

        final_list = []
        temp = layer.fields().names()

        for f in layer.getFeatures():
            temporary_dictionary = {}

            for attr in temp:

                temporary_dictionary[attr] = f[attr]

            temporary_dictionary["geometry"] = wkt.loads(f.geometry().asWkt())

            final_list.append(temporary_dictionary)

        return final_list


    def __from_list_of_dict_to_layer(self,feat_list):
        """Transform a list into a QgsVectorLayer (memory) based on this vectorLayer model (self.initial_layer) 

        Input:
        feat_list -- A list composed of dictionnary (1 dictionnary = 1 feature) with at least a 'geometry' parameter in each 

        Output:
        mem_layer -- A QgsVectorLayer filled with the elements in feat_list
        
        """

        epsg = self.initial_layer.crs().postgisSrid()

        mem_layer = QgsVectorLayer("Linestring?crs=EPSG:" + str(epsg),
                                    "temp",
                                    "memory")

        pr = mem_layer.dataProvider()
        layer_fields = self.initial_layer.fields()
        pr.addAttributes(layer_fields)

        mem_layer.updateFields()

        for obj in feat_list:
            f= QgsFeature()
            geom = QgsGeometry().fromWkt(obj["geometry"].wkt)
            f.setGeometry(geom)

            attributes_list = []

            for attr in layer_fields.names():
                attributes_list.append(obj[attr])

            f.setAttributes(attributes_list)
            pr.addFeature(f)

        mem_layer.updateExtents()

        return mem_layer



        




        #====================================================
        # Perso
        
        # self.reduced_layer.removeSelection()
        
        """
        i =0
        for f in self.reduced_layer.getFeatures():
            if i == 0:
                print(f.id())
                self.reduced_layer.select(f.id())
                i+=1
                geom = f.geometry()
                #print(geom)

        for f in self.reduced_layer.getSelectedFeatures():
            print(f.id())"""

        #Créé un nouveau layer et l'ajoute
        #memory_layer = self.initial_layer.materialize(QgsFeatureRequest().setFilterFids(self.initial_layer.selectedFeatureIds()))
        #QgsProject.instance().addMapLayer(memory_layer)

        

    