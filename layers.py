from .pathLayer import *
from .networkLayer import *

class Layers:
    

    def __init__(self,_path_layer,_network_layer):
        #init classes
        self.path_layer = PathLayer(_path_layer)
        self.network_layer = NetworkLayer(_network_layer)

    def reduce_network_layer(self, range, progression = None):
        """Makes a spatial selection on the network layer."""

        #check : boundingBoxOfSelected

        if(progression is not None):
            progression.emit(10)

        #Buffer's creation
        self.path_layer.create_buffer(range)

        if(progression is not None):
            progression.emit(50)

        #Spatial selection
        self.network_layer.select_intersection_trajectory(self.path_layer.buffer)

        #print("Network layer successfuly reduced")


    def correct_network_layer_topology(self, progression = None):
        """Correct the topology to prevent futures error. """

        self.network_layer.correct_topology(progression)

    def reduce_Path_layer(self,speedRowName):
        """Merge stationnary point. """

        self.path_layer.merge_stationary_point(speedRowName)


    def match(self):

        self.network_layer.add_attribute_to_layers()

        #self.network_layer.layer
        matching = mapMatching(self.network_layer.layer,self.path_layer.layer)

        self.network_layer.find_path(matching)

        self.path_layer.adjust_point_on_map(matching)


    def reSelect_path(self):
        self.network_layer.select_possible_path()


    def apply_modification(self):
        self.network_layer.change_possible_path()
        self.path_layer.reset_path()

        layer = self.network_layer.create_vector_from_path()

        matching = mapMatching(None,self.path_layer.layer, layer )

        self.path_layer.adjust_point_on_map(matching)
        


        