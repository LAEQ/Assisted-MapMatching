import os
import unittest
from unittest.mock import MagicMock

from model.utils.layerTraductor import *
from model.matcheur import *

from test.fixtures.layers import LayerFixtures
from test.utilities import get_qgis_app
QGIS_APP = get_qgis_app()

class TestMatcheur(unittest.TestCase):

    def setUp(self) -> None:
        self.cur_dir = os.path.dirname(__file__)
        self.fixtures = LayerFixtures()
        self.matcheur = Matcheur()

    def test_set_parameters(self):
        self.matcheur.set_parameters(12.5, 0.3)
        self.assertEqual(12.5, self.matcheur.searching_radius)
        self.assertEqual(0.3, self.matcheur.sigma)

    def test_set_layers(self):
        l1 = self.fixtures.network_1()
        l2 = self.fixtures.points_1()

        self.matcheur.set_layers(l1,l2)

        self.assertEqual(l1, self.matcheur.network_layer)
        self.assertEqual(l2, self.matcheur.path_layer)

    def test_verify_input(self):
        l1 = self.fixtures.network_1()
        l2 = self.fixtures.points_1()

        self.matcheur = Matcheur(l1, l2, "fid")

        #Normal case        
        self.matcheur.searching_radius = 12
        self.matcheur.sigma = 10

        res = self.matcheur.verify_input()
        self.assertEqual(True, res)

        #searching radius = 0
        self.matcheur.searching_radius = 0
        res = self.matcheur.verify_input()
        self.assertEqual(True, res)

        #wrong searching radius
        self.matcheur.searching_radius = None
        res = self.matcheur.verify_input()
        self.assertEqual("matcheur.error_searching_radius", res)

        self.matcheur.searching_radius = -10
        res = self.matcheur.verify_input()
        self.assertEqual("matcheur.error_searching_radius", res)

        #wrong sigma
        self.matcheur.searching_radius = 12
        self.matcheur.sigma = None
        res = self.matcheur.verify_input()
        self.assertEqual("matcheur.error_sigma", res)

        self.matcheur.sigma = 0
        res = self.matcheur.verify_input()
        self.assertEqual("matcheur.error_sigma", res)

        self.matcheur.sigma = -10
        res = self.matcheur.verify_input()
        self.assertEqual("matcheur.error_sigma", res)