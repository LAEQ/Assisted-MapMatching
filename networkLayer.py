from qgis import processing
from qgis.core import *
from qgis.PyQt.QtCore import QVariant

from .topology import *


from .mapMatching import mapMatching

from .layerTraductor import *

"""
This class take care of the network layer
It has 2 objects:
It's initial layer: layer
The reduced one : reduced_layer

"""

class NetworkLayer:


    def __init__(self, _layer):
        self.initial_layer = _layer
        self.layer = self.initial_layer #dans un premier temps
        self.possible_path = None #selected path in mapMatching.py


    def select_intersection_trajectory(self,buffer):
        """Reduce the network layer features by only keeping the line intersecting the buffer

        Input:
        buffer -- A buffer of type QgsVectorLayer

        """

        #Sécurité: on commence à vide
        self.initial_layer.removeSelection()

        test = processing.run("qgis:selectbylocation", {'INPUT': self.initial_layer, 'PREDICATE': 0, 'INTERSECT' : buffer , 'METHOD' : 0})
        
        reduced_layer = self.initial_layer.materialize(QgsFeatureRequest().setFilterFids(self.initial_layer.selectedFeatureIds()))
        self.initial_layer.removeSelection()

        QgsProject.instance().layerTreeRoot().findLayer(self.initial_layer.id()).setItemVisibilityChecked(False)

        self.layer = reduced_layer
        self.layer.setName("Reduced network")

        #Temporary line to show the progression
        #QgsProject.instance().addMapLayer(self.layer)
        
        
        #print("Reduced layer: ")
        

    def correct_topology(self, call_close_call = False, progression = None):
        """Correct the topology of the layer."""

        if(progression is not None):
            progression.emit(5)

        shapely_dict = layerTraductor.from_vector_layer_to_list_of_dict(self.layer)

        #if(progression is not None):
            #progression.emit(10)
        
        #We truncate all the points value 
        corrected_list = simplify_coordinates(shapely_dict,3)

        #if(progression is not None):
            #progression.emit(20)

        #We split the loops  (i.e: roundabouts)
        corrected_list = cut_loops(corrected_list)

        #if(progression is not None):
            #progression.emit(40)

        #We take care of the intersection
        corrected_list = deal_with_danglenodes(corrected_list)

        corrected_list = deal_with_intersections(corrected_list)

        if(progression is not None):
            progression.emit(1)

        #NB: La ligne ci dessous prend un temps monstre
        #We connect roads wich extremities are close to each other
        if(call_close_call):
            corrected_list = deal_with_closecall(corrected_list,progression)

        #if(progression is not None):
            #progression.emit(80)

        
        lay = layerTraductor.from_list_of_dict_to_layer(corrected_list,self.layer)

        #if(progression is not None):
            #progression.emit(90)

        QgsProject.instance().removeMapLayer(self.layer)

        self.layer = lay

        #Temporary line : Ajout de la couche à l'application
        QgsProject.instance().addMapLayer(self.layer)
        

    def find_path(self, matching, progression = None): 
        
        matching.find_best_path_in_network()

        self.possible_path = matching.tag_id

        self.select_possible_path()


    def add_attribute_to_layers(self, attribute_name = 'joID'):

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


        
        

    def select_possible_path(self):
        if(self.possible_path) == None:
            print("error : path not created yet")
            return

        self.layer.selectByExpression('"joID" in (' +','.join(self.possible_path)+ ')' )




    def change_possible_path(self):
        self.possible_path = [str(feat['joID']) for feat in self.layer.getSelectedFeatures()]


    def create_vector_from_path(self):

        layer = processing.run("native:saveselectedfeatures", {'INPUT': self.layer, 'OUTPUT': 'memory:'})['OUTPUT']
        layer.setName("path for matching")

        return layer






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

        

    