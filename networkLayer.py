

class NetworkLayer:


    def __init__(self, _layer):
        self.layer = _layer

        #copy the layer and create a new one
        _layer.selectAll()
        self.layer = processing.run("native:saveselectedfeatures", {'INPUT': _layer, 'OUTPUT': 'memory:'})['OUTPUT']
        _layer.removeSelection()

    def create_buffer(self, range):
        pass
    