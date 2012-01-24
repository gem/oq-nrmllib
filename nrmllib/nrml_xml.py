# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright (c) 2010-2011, GEM Foundation.
#
# Nrmllib is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License version 3
# only, as published by the Free Software Foundation.
#
# Nrmllib is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License version 3 for more details
# (a copy is included in the LICENSE file that accompanied this code).
#
# You should have received a copy of the GNU Lesser General Public License
# version 3 along with Nrmllib. If not, see
# <http://www.gnu.org/licenses/lgpl-3.0.txt> for a copy of the LGPLv3 License.

"""
The purpose of this module is to provide constants,
and some utility function to deal with nrml (xml file format)
and the retrieval of nrml schema path or nrml input files.
"""

import os


ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

SCHEMA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__),
        '../nrml/schema'))

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__),
        '../tests/data'))

FILE_NAME_ERROR = "Unknown filename"

NRML_NS = 'http://openquake.org/xmlns/nrml/0.3'
GML_NS = 'http://www.opengis.net/gml'

NRML = "{%s}" % NRML_NS
GML = "{%s}" % GML_NS

NSMAP = {None: NRML_NS, "gml": GML_NS}

ROOT = "%snrml" % NRML
SOURCE_MODEL = "%ssourceModel" % NRML
CONFIG = "%sconfig" % NRML
TYPE = "type"

AREA_SOURCE = "%sareaSource" % NRML
GML_ID = "%sid" % GML
GML_NAME = "%sname" % GML
TECTONIC_REGION = "%stectonicRegion" % NRML

AREA_BOUNDARY = "%sareaBoundary" % NRML
POLYGON = "%sPolygon" % GML
EXTERIOR = "%sexterior" % GML
LINEAR_RING = "%sLinearRing" % GML
LINEAR_RING_NAME = "srsName"
POS_LIST = "%sposList" % GML

RUPTURE_RATE_MODEL = "%sruptureRateModel" % NRML

TRUNCATED_GUTEN_RICHTER = "%struncatedGutenbergRichter" % NRML

A_VALUE_CUMULATIVE = "%saValueCumulative" % NRML
B_VALUE = "%sbValue" % NRML
MIN_MAGNITUDE = "%sminMagnitude" % NRML
MAX_MAGNITUDE = "%smaxMagnitude" % NRML

STRIKE = "%sstrike" % NRML
DIP = "%sdip" % NRML
RAKE = "%srake" % NRML

RUPTURE_DEPTH_DISTRIB = "%sruptureDepthDistribution" % NRML
MAGNITUDE = "%smagnitude" % NRML
DEPTH = "%sdepth" % NRML

HYPOCENTRAL_DEPTH = "%shypocentralDepth" % NRML

SIMPLE_FAULT_SOURCE = "%ssimpleFaultSource" % NRML
RAKE = "%srake" % NRML
DIP = "%sdip" % NRML
SIMPLE_FAULT_GEOMETRY = "%ssimpleFaultGeometry" % NRML
UPPER_SEISMOGENIC_DEPTH = "%supperSeismogenicDepth" % NRML
LOWER_SEISMOGENIC_DEPTH = "%slowerSeismogenicDepth" % NRML

COMPLEX_FAULT_SOURCE = "%scomplexFaultSource" % NRML
EVENLY_DISCRETIZED_INC_MFD = "%sevenlyDiscretizedIncrementalMFD" % NRML
BIN_SIZE = "binSize"
MIN_VAL = "minVal"
COMPLEX_FAULT_GEOMETRY = "%scomplexFaultGeometry" % NRML
FAULT_TOP_EDGE = "%sfaultTopEdge" % NRML
FAULT_BOTTOM_EDGE = "%sfaultBottomEdge" % NRML

SIMPLE_POINT_SOURCE = "%spointSource" % NRML
LOCATION = "%slocation" % NRML
POINT = "%sPoint" % GML
SRS_NAME = "srsName"
POS = "%spos" % GML

def get_data_path(filename, dirname):
    """Return the data path of files used in test."""
    return os.path.join(dirname, filename)
