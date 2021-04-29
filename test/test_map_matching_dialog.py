# coding=utf-8
"""Dialog test.

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""
import unittest
from random import randint
from unittest.mock import MagicMock

from qgis.core import QgsVectorLayer, QgsField

from qgis.PyQt.QtWidgets import QDialogButtonBox, QDialog
from qgis.PyQt.QtCore import QVariant
from map_matching_dialog import MapMatchingDialog
from model.layer_manager import LayerManager
from test.fixtures.layers import LayerFixtures
from test.utilities import get_qgis_app

QGIS_APP = get_qgis_app()


class MapMatchingDialogTest(unittest.TestCase):
    """Test dialog works."""

    def setUp(self):
        """Runs before each test."""
        self.dialog = MapMatchingDialog(None)
        self.manager = LayerManager()
        self.dialog.set_manager(self.manager)
        self.fixtures = LayerFixtures()

    def tearDown(self):
        """Runs after each test."""
        self.dialog = None

    def test_update(self):
        magic_points = self.fixtures.points()
        magic_network = [self.fixtures.network_1()]
        self.manager.path_layers = MagicMock(return_value=magic_points)
        self.manager.network_layers = MagicMock(return_value=magic_network)
        self.dialog.update()
        self.assertEqual(2, self.dialog.combo_path.count())
        self.assertEqual(1, self.dialog.combo_network.count())


    # def test_dialog_add_path(self):
    #     layer = QgsVectorLayer("Point?crs=EPSG:4326", "layer name you like", "memory")
    #     self.dialog.add_path(layer)
    #     self.assertEqual(1, self.dialog.combo_path.count())
    #     self.assertEqual(0, self.dialog.combo_network.count())
    #
    # def test_dialog_add_network(self):
    #     layer = QgsVectorLayer("Point?crs=EPSG:4326", "layer name you like", "memory")
    #     self.dialog.add_network(layer)
    #     self.assertEqual(0, self.dialog.combo_path.count())
    #     self.assertEqual(1, self.dialog.combo_network.count())

    # def test_oid_speed_combo_on_path_changed(self):
    #     """
    #     Test combo oid and speed are updated when a path added
    #     """
    #     layer = generate_vector_path_4_fields()
    #
    #     self.assertEqual(0, self.dialog.combo_oid.count())
    #     self.dialog.add_path(layer)
    #     self.assertEqual(4, self.dialog.combo_oid.count())
    #     self.assertEqual(4, self.dialog.combo_speed.count())
    #
    # def test_oid_speed_combo_on_path_updated(self):
    #     """
    #     Test combo oid and speed are updated when a second path  is selected
    #     """
    #     layer = generate_vector_path_4_fields()
    #     self.dialog.add_path(layer)
    #
    #     layer2 = generate_vector_path_8_fields()
    #     self.dialog.add_path(layer2)
    #
    #     self.assertEqual(4, self.dialog.combo_oid.count())
    #     self.assertEqual(4, self.dialog.combo_speed.count())
    #
    #     self.dialog.combo_path.setCurrentIndex(1)
    #     self.assertEqual(8, self.dialog.combo_oid.count())
    #     self.assertEqual(8, self.dialog.combo_speed.count())


if __name__ == "__main__":
    suite = unittest.makeSuite(MapMatchingDialogTest)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

