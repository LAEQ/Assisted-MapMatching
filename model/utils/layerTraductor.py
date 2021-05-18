from shapely import wkt
from shapely.geometry import shape
from qgis.core import QgsVectorLayer, QgsFeature, QgsGeometry
import json

class layerTraductor:


    @staticmethod
    def from_vector_layer_to_list_of_dict(layer):
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
            
            tempa = f.geometry().asJson()

            temporary_dictionary["geometry"] = shape(json.loads(tempa))

            final_list.append(temporary_dictionary)

        return final_list

    @staticmethod
    def from_list_of_dict_to_layer(feat_list,layer_patern,type_layer = "Linestring",name = "new layer"):
        """Transform a list into a QgsVectorLayer (memory) based on this vectorLayer model (self.initial_layer) 

        Input:
        feat_list -- A list composed of dictionnary (1 dictionnary = 1 feature) with at least a 'geometry' parameter in each 

        Output:
        mem_layer -- A QgsVectorLayer filled with the elements in feat_list

        """

        epsg = layer_patern.crs().postgisSrid()

        typ = type_layer+"?crs=EPSG:"+ str(epsg)

        mem_layer = QgsVectorLayer(typ,name,"memory")

        pr = mem_layer.dataProvider()
        layer_fields = layer_patern.fields()
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

    @staticmethod
    def order_list_of_dict(feat_list,column_name = "OID"):
        """Sort a list according to it's OID column"""
        return sorted(feat_list,key= lambda obj: obj[column_name])