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


    def correct_network_layer_topology(self, close_call_tolerance = 0.3, inter_dangle_tolerance= 0.01, progression = None):
        """Correct the topology to prevent futures error. """

        self.network_layer.correct_topology(close_call_tolerance, inter_dangle_tolerance,progression)


    def reduce_Path_layer(self,speedRowName,speed_limit):
        """Merge stationnary point. """

        self.path_layer.merge_stationary_point(speedRowName, speed_limit)


    def match_speed(self, matching, speed_column_name):
        """ Start the matching algorithm based on speed """

        self.network_layer.find_path(matching)

        self.path_layer.speed_point_matching(matching,speed_column_name)


    def match_closest(self,matching):
        """ Start the matching algorithm to the closest position on the line """

        self.network_layer.find_path(matching)

        self.path_layer.closest_point_matching(matching)


    def match_by_distance(self,matching):
        """ Start the matching algorithm based on the distance between each points """

        self.network_layer.find_path(matching)

        self.path_layer.distance_point_matching(matching)



    def reSelect_path(self):
        """ Select on the canvas the path used by the last matching """

        self.network_layer.select_possible_path()


    def apply_modification(self,type_of_matching,search_rad,sigma, speed_column_name = None, OID = "OID"):
        """ Change the possible path and recalculate the position of the points """

        self.network_layer.change_possible_path()
        self.path_layer.reset_path()

        layer = self.network_layer.create_vector_from_path()

        matching = mapMatching(None,self.path_layer.layer, layer, _OID = OID )
        matching.setParameters(search_rad,sigma)

        if type_of_matching == "Matching with Speed" and speed_column_name != None:
            self.path_layer.speed_point_matching(matching,speed_column_name)

        elif type_of_matching == "Matching closest":
            self.path_layer.closest_point_matching(matching)

        elif type_of_matching == "Matching by distance":
            self.path_layer.distance_point_matching(matching)

        
        


        