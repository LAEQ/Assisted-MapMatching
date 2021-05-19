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
from model.ui.layer_manager import LayerManager
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


    def test_update_layer_box(self):
        magic_points = self.fixtures.points()
        magic_network = [self.fixtures.network_1()]
        self.manager.get_path_layers = MagicMock(return_value=magic_points)
        self.manager.get_network_layers = MagicMock(return_value=magic_network)
        self.dialog.update_layer_box()
        self.assertEqual(2, self.dialog.combo_path.count())
        self.assertEqual(1, self.dialog.combo_network.count())


    def test_clear_combo(self):
        magic_points = self.fixtures.points()
        magic_network = [self.fixtures.network_1()]
        self.manager.get_path_layers = MagicMock(return_value=magic_points)
        self.manager.get_network_layers = MagicMock(return_value=magic_network)
        self.dialog.update_layer_box()
        self.dialog.clear_combo()
        self.assertEqual(0, self.dialog.combo_path.count())
        self.assertEqual(0, self.dialog.combo_network.count())
        self.assertEqual(0, self.dialog.combo_oid.count())
        self.assertEqual(0, self.dialog.combo_speed.count())


    def test_path_changed(self):
        magic_points = self.fixtures.points()
        magic_network = self.fixtures.networks()
        magic_fields = self.fixtures.points_fields_1()
        self.manager.get_path_layers = MagicMock(return_value=magic_points)
        self.manager.get_network_layers = MagicMock(return_value=magic_network)
        self.manager.get_path_attributes = MagicMock(return_value=magic_fields)
        self.dialog.update_layer_box()
        self.dialog.combo_path.setCurrentIndex(1)
        #2 because points_fields_1 has only 2 fields of type integer /integer48...
        self.assertEqual(2, self.dialog.combo_oid.count())


    def test_update_matched_path_box(self):
        index = self.dialog.combo_algo_matching.findText("Matching with Speed")
        self.dialog.combo_algo_matching.removeItem(index)

        self.dialog.check_speed.isChecked = MagicMock(return_value = True)
        self.dialog.update_matching_box()

        self.assertEqual(3, self.dialog.combo_algo_matching.count())
        self.assertEqual("Matching with Speed", self.dialog.combo_algo_matching.currentText())

        self.dialog.check_speed.isChecked = MagicMock(return_value = False)
        self.dialog.update_matching_box()

        self.assertEqual(2, self.dialog.combo_algo_matching.count())
        self.assertNotEqual("Matching with Speed", self.dialog.combo_algo_matching.currentText())


    def test_update_matched_path_box(self):

        #empty matched layers
        self.manager.get_matched_layers = MagicMock(return_value=[])
        self.dialog.update_matched_path_box()
        self.assertEqual(0, self.dialog.combo_matched_track.count())

        #filled matched layers
        magic_points = self.fixtures.points()
        self.manager.get_matched_layers = MagicMock(return_value=magic_points)
        self.dialog.update_matched_path_box()
        self.assertEqual(len(magic_points), self.dialog.combo_matched_track.count())

    def test_restore_state(self):
        magic_points = self.fixtures.points()
        magic_network = self.fixtures.networks()
        self.manager.get_path_layers = MagicMock(return_value=magic_points)
        self.manager.get_network_layers = MagicMock(return_value=magic_network)
        self.dialog.update_layer_box()

        self.dialog.manager.selected_path = "points_2.gpkg"
        self.dialog.manager.selected_network = "network_2.gpkg"
        self.dialog.manager.OID = "fid"
        self.dialog.manager.speed = "Speed"

        self.dialog.combo_path.setCurrentText("")

        self.dialog.restore_state()

        self.assertEqual("points_2.gpkg", self.dialog.combo_path.currentText())
        self.assertEqual("network_2.gpkg", self.dialog.combo_network.currentText())
        self.assertEqual("fid", self.dialog.combo_oid.currentText())
        self.assertEqual("Speed", self.dialog.combo_speed.currentText())





if __name__ == "__main__":
    suite = unittest.makeSuite(MapMatchingDialogTest)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

