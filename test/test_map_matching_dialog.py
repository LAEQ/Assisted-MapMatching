# coding=utf-8
"""Dialog test.

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""
import unittest
from qgis.core import QgsVectorLayer
from qgis.PyQt.QtWidgets import QDialogButtonBox, QDialog
from map_matching_dialog import MapMatchingDialog
from test.utilities import get_qgis_app

QGIS_APP = get_qgis_app()


class MapMatchingDialogTest(unittest.TestCase):
    """Test dialog works."""

    def setUp(self):
        """Runs before each test."""
        self.dialog = MapMatchingDialog(None)

    def tearDown(self):
        """Runs after each test."""
        self.dialog = None

    @unittest.skip("Must be updated or deleted before merging to master.")
    def test_dialog_ok(self):
        """Test we can click OK."""

        button = self.dialog.button_box.button(QDialogButtonBox.Ok)
        button.click()
        result = self.dialog.result()
        self.assertEqual(result, QDialog.Accepted)

    @unittest.skip("Must be updated or deleted before merging to master.")
    def test_dialog_cancel(self):
        """Test we can click cancel."""
        button = self.dialog.button_box.button(QDialogButtonBox.Cancel)
        button.click()
        result = self.dialog.result()
        self.assertEqual(result, QDialog.Rejected)

    def test_dialog_add_path(self):
        layer = QgsVectorLayer("Point?crs=EPSG:4326", "layer name you like", "memory")
        self.dialog.add_path(layer)
        self.assertEqual(1, self.dialog.combo_path.count())
        self.assertEqual(0, self.dialog.combo_network.count())

    def test_dialog_add_network(self):
        layer = QgsVectorLayer("Point?crs=EPSG:4326", "layer name you like", "memory")
        self.dialog.add_network(layer)
        self.assertEqual(0, self.dialog.combo_path.count())
        self.assertEqual(1, self.dialog.combo_network.count())


if __name__ == "__main__":
    suite = unittest.makeSuite(MapMatchingDialogTest)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

