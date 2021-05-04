# import some modules used in the example
from qgis.core import *
from PyQt5 import QtCore, QtGui
import traceback
import time
from .layers import Layers

class Worker(QtCore.QObject):
    '''Multithreading worker: put in background heavy work'''


    def __init__(self, layers):
        QtCore.QObject.__init__(self)
        self.layers = layers
        self.killed = False


    def run_reduce_network_layer(self):
        ret = None
        try:
            
            self.layers.reduce_network_layer(self.range_buffer,self.progress)

                    
            if self.killed is False:

                ret = "reduce_network_layer"
                self.progress.emit(100)
                

        except Exception as e:
            # forward the exception upstream
            self.error.emit(e, "Error reduce network:  " + traceback.format_exc())


        self.finished.emit(ret)


    def run_correct_topology(self):
        ret = None
        try:
            
            self.layers.correct_network_layer_topology(self.progress)

            
                    
            if self.killed is False:

                ret = "correct_topology"
                self.progress.emit(100)
                

        except Exception as e:
            # forward the exception upstream
            self.error.emit(e, "Error topology:  " + traceback.format_exc())

        self.finished.emit(ret)


    def run_map_matching(self):
        ret = None
        try:
            
            self.layers.match(self.progress)

            
                    
            if self.killed is False:

                ret = "matching"
                self.progress.emit(100)
                

        except Exception as e:
            # forward the exception upstream
            self.error.emit(e, "Error matching:  " + traceback.format_exc())

        self.finished.emit(ret)


    finished = QtCore.pyqtSignal(object)
    error = QtCore.pyqtSignal(Exception, basestring)
    progress = QtCore.pyqtSignal(float)


    def kill(self):
        self.killed = True

    def add_range(self,r):
        self.range_buffer= r



        


