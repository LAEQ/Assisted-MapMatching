# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MapMatching
                                 A QGIS plugin
 to come
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2021-04-13
        copyright            : (C) 2021 by LAEQ - INRS
        email                : tocome@email.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load MapMatching class from file MapMatching.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .map_matching import MapMatching
    return MapMatching(iface)
