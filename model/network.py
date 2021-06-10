from qgis import processing
from qgis.core import QgsVectorLayer, QgsFeatureRequest, QgsField
from qgis.PyQt.QtCore import QVariant

# Import own class
from .utils.layerTraductor import *
from .topology import *
from .matcheur import *


class NetworkLayer:
    """This class modify directly the selected network layer
    
    Parameters:
    initial_layer: An object of type QgsVectorLayer. It doesn't change through the process
    layer: An object of type QgsVectorLayer. Represent the network layer modified through the process
    """

    def __init__(self, _layer):
        self.initial_layer = _layer
        self.layer = self.initial_layer


    def select_intersection_trajectory(self, buffer: QgsVectorLayer):
        """Reduce the network layer features by only keeping the line 
           intersecting the buffer.

        Input:
        buffer -- A buffer of type QgsVectorLayer
        """

        # Security: we start with no selection
        self.initial_layer.removeSelection()

        # Select on initial layer every road that intersect buffer
        try:
            test = processing.run("qgis:selectbylocation",
                                 {'INPUT': self.initial_layer, 
                                 'PREDICATE': 0, 'INTERSECT': buffer, 
                                 'METHOD': 0})
        except:
            # print("Error processing in select_intersection_trajectory (Network.py)")
            return "network.select_intersection_trajectory.processing"

        # Create a QgsVectorLayer from a selection
        reduced_layer = self.initial_layer.materialize(
            QgsFeatureRequest().setFilterFids(self.initial_layer.selectedFeatureIds()))

        self.initial_layer.removeSelection()
        reduced_layer.setProviderEncoding("UTF-8")
        reduced_layer.setName("Reduced network")
        self.layer = reduced_layer

        # Success
        return None

    def correct_topology(self, close_call_tol: float, inter_dangle_tol: float):
        """Correct the topology of the layer."""

        # Conversion to shapely dict
        shapely_dict = from_vector_layer_to_list_of_dict(self.layer)

        if isinstance(shapely_dict, str):
            return "network.correct_topology." + shapely_dict

        # We truncate all the points value
        corrected_list = simplify_coordinates(shapely_dict, 3)

        # We split the loops  (i.e: roundabouts)
        corrected_list = cut_loops(corrected_list)

        # We take care of the intersection
        corrected_list = deal_with_danglenodes(corrected_list, inter_dangle_tol)
        if corrected_list == None:
            return 
        
        corrected_list = deal_with_intersections(corrected_list, inter_dangle_tol)

        # We connect roads wich extremities are close to each other
        corrected_list = deal_with_closecall(corrected_list, close_call_tol)

        # Conversion to QgsVectorLayer
        self.layer = from_list_of_dict_to_layer(corrected_list,
                                                               self.layer,
                                                               "LineString",
                                                               "corrected layer")

        if isinstance(self.layer, str):
            return "network.correct_topology." + self.layer

        # Success
        return None

    def add_attribute_to_layers(self, attribute_name: str = 'joID'):
        """ Create a new column to the network_layer indexed from 0 
            to the number of feature in the layer.

        Input:
        attribute_name : -- A string that represent the name of the new column
        """

        # Verify input validity
        if attribute_name == "" or attribute_name == None:
            return "network.add_attribute_to_layers.empty_attribute_name"

        # add a new field to the layer
        provider = self.layer.dataProvider()
        provider.addAttributes([QgsField(attribute_name, QVariant.Int)])
        self.layer.updateFields()

        length = len(self.layer.fields().names()) - 1

        features = self.layer.getFeatures()
        # Complete the field for every features
        self.layer.startEditing()
        i = 0
        for f in features:
            tesid = f.id()
            attr_value = {length:i}
            provider.changeAttributeValues({tesid: attr_value})
            i += 1
        self.layer.commitChanges()

        # Success
        return None

    def find_path(self, matcheur: Matcheur): 
        """Find a possible route 
        
        Input: 
        matcheur :  -- An object of class Matcheur 
        """

        result = matcheur.find_best_path_in_network()

        if isinstance(result, str):
            return "network.find_path." + result

        self.possible_path = matcheur.tag_id

        self.select_possible_path()

        # Success
        return None

    def select_possible_path(self):
        """ Select in the network_layer the path recorded at the last matching."""

        if (self.possible_path) == None:
            return "network.select_possible_path.no_path_registered"
        try:
            self.layer.selectByExpression('"joID" in (' +
                                          ','.join(self.possible_path) + ')')
        except:
            print("Seems like the network has been deleted")

        # Success
        return None

    def change_possible_path(self):
        """ Change the possible trajectory recorded """
        
        if self.layer.selectedFeatureCount() <= 0:
            return "network.change_possible_path.no_selection"

        self.possible_path = [str(feat['joID']) for feat in self.layer.getSelectedFeatures()]

        # Success
        return None

    def create_vector_from_path(self) -> QgsVectorLayer:
        """Create a QgsVectorLayer from the selected features """

        layer = processing.run(
            "native:saveselectedfeatures",
            {'INPUT': self.layer, 'OUTPUT': 'memory:'})['OUTPUT']
        layer.setName("path for matching")

        return layer