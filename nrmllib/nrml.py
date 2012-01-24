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
The purpose of this module is to provide objects
capable of parsing and serializing specific flavours
of the NRML data format.
"""

import os
from lxml import etree

from nrmllib                import nrml_xml
from nrmllib.source_model   import AreaSource
from nrmllib.source_model   import POINT
from nrmllib.source_model   import AREA_BOUNDARY
from nrmllib.source_model   import TRUNCATED_GUTEN_RICHTER
from nrmllib.source_model   import RUPTURE_RATE_MODEL
from nrmllib.source_model   import MAGNITUDE
from nrmllib.source_model   import RUPTURE_DEPTH_DISTRIB

XML_NODE = 1


class NRMLReader(object):
    """
    NRMLReader object allows to parse source model
    in a nrml file in an iterative way. NRMLReader
    generates area source objects for each area
    source element in the parsed document.
    """

    def __init__(self, filename, schema):
        """
        Constructor
        :param filename: nrml input filename
        :type filename: string
        :param schema: nrml schema
        :type schema: string
        """

        self.filename = filename
        self.schema = etree.XMLSchema(etree.parse(schema))

        self.tag_action = {nrml_xml.AREA_SOURCE: _parse_area_source}

    def read(self):
        """
        Generator method, yields AreaSource
        object for every area source element
        in the nrml input file.
        :returns: source model object
        :rtype: py:class:: AreaSource
        """

        with open(self.filename, 'rb') as nrml_file:
            for source_model in etree.iterparse(nrml_file, schema=self.schema):
                tag = source_model[XML_NODE].tag
                if tag in self.tag_action:
                    yield self.tag_action[tag](source_model[XML_NODE])


def _parse_area_source(as_elem):
    """
    Creates an AreaSource object by
    extracting data contained in an
    area source element.
    :param as_elem: area source element
    :type as_elem: lxml.etree._Element
    :returns: area source object
    :rtype: py:class::AreaSource
    """

    area_source = AreaSource()

    area_source.nrml_id = as_elem.getparent().getparent().get(
            nrml_xml.GML_ID)

    area_source.source_model_id = as_elem.getparent().get(
            nrml_xml.GML_ID)

    area_source.area_source_id = as_elem.get(
        nrml_xml.GML_ID)

    area_source.name = as_elem.find(
        nrml_xml.GML_NAME).text

    area_source.tectonic_region = as_elem.find(
        nrml_xml.TECTONIC_REGION).text

    area_source.area_boundary = _parse_area_boundary(
        as_elem.find(nrml_xml.AREA_BOUNDARY))

    area_source.rupture_rate_model = _parse_rupture_rate_model(
        as_elem.find(nrml_xml.RUPTURE_RATE_MODEL))

    area_source.rupture_depth_dist = _parse_rupture_depth_distrib(
        as_elem.find(nrml_xml.RUPTURE_DEPTH_DISTRIB))

    area_source.hypocentral_depth = float(as_elem.find(
        nrml_xml.HYPOCENTRAL_DEPTH).text)

    as_elem.clear()

    return area_source


def _parse_area_boundary(area_boundary_elem):
    """
    Creates an AreaBounday object by extracting
    data contained in an area boundary element.
    :param area_boundary_elem: area boundary element
    :type area_boundary_elem: lxml.etree._Element
    :returns: area boundary object
    :rtype: py:class::AreaBoundary
    """

    srs_name = area_boundary_elem.find('.//%s' %
        nrml_xml.LINEAR_RING).get(nrml_xml.LINEAR_RING_NAME)

    pos_list_values = area_boundary_elem.find(
        './/%s' % nrml_xml.POS_LIST).text.split()
    pos_list = [POINT(float(pos_list_values[i]), float(pos_list_values[i + 1]))
            for i in xrange(0, len(pos_list_values), 2)]

    area_boundary_elem.clear()

    return AREA_BOUNDARY(srs_name, pos_list)


def _parse_rupture_rate_model(rupture_rate_model_elem):
    """
    Creates a RuptureRateModel object by extracting
    data contained in an rupture rate model element.
    :param rupture_rate_model_elem: rupture rate model element
    :type rupture_rate_model: lxml.etree._Element
    :returns: rupture rate model object
    :rtype: py:class::RuptureRateModel
    """

    truncatd_gutenberg_rich_elem = rupture_rate_model_elem.find(
            nrml_xml.TRUNCATED_GUTEN_RICHTER)

    truncated_gutenberg_richter = TRUNCATED_GUTEN_RICHTER(
        float(truncatd_gutenberg_rich_elem.find(
            nrml_xml.A_VALUE_CUMULATIVE).text),
        float(truncatd_gutenberg_rich_elem.find(
            nrml_xml.B_VALUE).text),
        float(truncatd_gutenberg_rich_elem.find(
            nrml_xml.MIN_MAGNITUDE).text),
        float(truncatd_gutenberg_rich_elem.find(
            nrml_xml.MAX_MAGNITUDE).text),
        truncatd_gutenberg_rich_elem.get(nrml_xml.TYPE))

    rupture_rate_model = RUPTURE_RATE_MODEL(truncated_gutenberg_richter,
        float(rupture_rate_model_elem.find(nrml_xml.STRIKE).text),
        float(rupture_rate_model_elem.find(nrml_xml.DIP).text),
        float(rupture_rate_model_elem.find(nrml_xml.RAKE).text))

    truncatd_gutenberg_rich_elem.clear()
    rupture_rate_model_elem.clear()

    return rupture_rate_model


def _parse_rupture_depth_distrib(rdd_elem):
    """
    Creates a RuptureDepthDistrib object by extracting
    data contained in an rupture depth distribution
    element.
    :param rdd_elem: rupture depth distribution element
    :type rdd_elem: lxml.etree._Element
    :returns: rupture depth distribution object
    :rtype: py:class::RuptureDepthDistrib
    """

    magnitude_elem = rdd_elem.find(nrml_xml.MAGNITUDE)
    magnitude = MAGNITUDE(
            magnitude_elem.get(nrml_xml.TYPE),
            [float(value) for value in rdd_elem.find(
                    nrml_xml.MAGNITUDE).text.split()])

    rupture_depth_distrib = RUPTURE_DEPTH_DISTRIB(
            magnitude,
            [float(value) for value in rdd_elem.find(
            nrml_xml.DEPTH).text.split()])

    rdd_elem.clear()

    return rupture_depth_distrib


class AreaSourceWriter(object):
    """
    AreaSourceWriter object allows to serialize a
    sequence of AreaSource objects in the nrml
    data format.
    """

    def __init__(self, filename):
        """
        Constructor
        :param filename: nrml input filename
        :type filename: string
        """

        dirname = os.path.dirname(filename)
        if not os.path.exists(dirname):
            raise IOError('Dir %s not found' %
                (os.path.abspath(dirname), ))
        self.filename = filename

    def serialize(self, area_sources):
        """
        Write area source definitions in the nrml file
        :param area_sources: area source objects
        :type area_sources: sequence of area source objects
        """

        root_elem = _write_header(area_sources)
        root_elem = _write_body(root_elem, area_sources)

        tree = etree.ElementTree(root_elem)
        tree.write(open(self.filename, 'w'),
            xml_declaration=True, encoding='utf-8',
            pretty_print=True)

def _write_header(area_sources):
    """
    Create nrml header elems
    :param area_sources: area source objects
    :type area_sources: sequence of area source objects
    :returns: root elem with attached header elements
    :rtype: lxml.etree._Element
    """

    # Every area_source definition has header attributes
    first_area_source_index = 0
    root_elem = etree.Element(nrml_xml.ROOT, nsmap=nrml_xml.NSMAP)
    root_elem.attrib[nrml_xml.GML_ID] = \
        area_sources[first_area_source_index].nrml_id

    source_model_elem = etree.SubElement(
        root_elem, nrml_xml.SOURCE_MODEL)
    source_model_elem.attrib[nrml_xml.GML_ID] = \
        area_sources[first_area_source_index].source_model_id

    config_elem = etree.SubElement(
        source_model_elem, nrml_xml.CONFIG)
    return root_elem

def _write_body(root_elem, area_sources):
    """
    Attach nrml body elements to the root element
    :param root_elem: root elem of nrml document
    :type root_elem: lxml.etree._Element
    :param area_sources: area source objects
    :type area_sources: sequence of area source objects
    :returns: root elem with attached body elements
    :rtype: lxml.etree._Element
    """

    source_model_elem = root_elem.find(nrml_xml.SOURCE_MODEL)
    for area_source in area_sources:
        source_model_elem.append(_area_source_elem(area_source))
    return root_elem

def _area_source_elem(area_source):
    """
    Create area source element by reading
    data from the area source object.
    :param area_source: area source object
    :type area_source: py:class:: AreaSource
    """

    area_source_elem = etree.Element(nrml_xml.AREA_SOURCE)
    area_source_elem.attrib[nrml_xml.GML_ID] = area_source.area_source_id

    name_elem = etree.SubElement(
        area_source_elem, nrml_xml.GML_NAME)
    name_elem.text = area_source.name

    tectonic_region_elem = etree.SubElement(
        area_source_elem, nrml_xml.TECTONIC_REGION)
    tectonic_region_elem.text = area_source.tectonic_region

    _write_area_boundary(area_source_elem, area_source.area_boundary)

    _write_rupture_rate_model(
        area_source_elem, area_source.rupture_rate_model)

    _write_rupture_depth_distrib(
        area_source_elem, area_source.rupture_depth_dist)

    hypocentral_depth_elem = etree.SubElement(
        area_source_elem, nrml_xml.HYPOCENTRAL_DEPTH)
    hypocentral_depth_elem.text = str(
        area_source.hypocentral_depth)

    return area_source_elem

def _write_area_boundary(container_elem, area_boundary):
    """
    Attach an area boundary element
    to the element container.
    :param container_elem: element which contains area boundary
    :type container_elem: lxml.etree._Element
    :param area_boundary: area boundary object
    :type area_boundary: py:class::AreaBoundary
    """

    area_boundary_elem = etree.SubElement(
        container_elem, nrml_xml.AREA_BOUNDARY)

    polygon_elem = etree.SubElement(
        area_boundary_elem, nrml_xml.POLYGON)

    exterior_elem = etree.SubElement(
        polygon_elem, nrml_xml.EXTERIOR)

    linear_ring_elem = etree.SubElement(
        exterior_elem, nrml_xml.LINEAR_RING)
    linear_ring_elem.attrib[nrml_xml.SRS_NAME] = area_boundary.srs_name

    pos_list_elem = etree.SubElement(
        linear_ring_elem, nrml_xml.POS_LIST)

    pos_list = []
    for point in area_boundary.pos_list:
        pos_list.append(point.lon)
        pos_list.append(point.lat)
    pos_list_elem.text = ' '.join(
        (str(value) for value in pos_list))

def _write_rupture_rate_model(container_elem,
    rupture_rate_model):
    """
    Attach a rupture rate model element
    to the element container.
    :param container_elem: element which contains rupture rate model
    :type container_elem: lxml.etree._Element
    :param rupture_rate_model: rupture rate model object
    :type rupture_rate_model: py:class::RuptureRateModel
    """

    rupture_rate_model_elem = etree.SubElement(
        container_elem, nrml_xml.RUPTURE_RATE_MODEL)

    _write_truncated_guten_richter(rupture_rate_model_elem,
            rupture_rate_model.truncated_gutenberg_richter)

    strike_elem = etree.SubElement(
            rupture_rate_model_elem, nrml_xml.STRIKE)
    strike_elem.text = str(rupture_rate_model.strike)

    dip_elem = etree.SubElement(
            rupture_rate_model_elem, nrml_xml.DIP)
    dip_elem.text = str(rupture_rate_model.dip)

    rake_elem = etree.SubElement(
            rupture_rate_model_elem, nrml_xml.RAKE)
    rake_elem.text = str(rupture_rate_model.rake)

def _write_truncated_guten_richter(container_elem,
    truncated_gutenberg_richter):
    """
    Attach a truncated gutenberg richter element
    to the element container.
    :param container_elem: element which contains truncated
     gutenberg richter
    :type container_elem: lxml.etree._Element
    :param truncated_gutenberg_richter: truncated_gutenberg richter object
    :type truncated_gutenberg_richter: py:class::TruncatedGutenRichter
    """

    truncatd_gutenberg_rich_elem = etree.SubElement(
        container_elem, nrml_xml.TRUNCATED_GUTEN_RICHTER)
    truncatd_gutenberg_rich_elem.attrib[nrml_xml.TYPE] = \
        truncated_gutenberg_richter.type_tgr

    a_value_elem = etree.SubElement(
        truncatd_gutenberg_rich_elem, nrml_xml.A_VALUE_CUMULATIVE)
    a_value_elem.text = \
        str(truncated_gutenberg_richter.a_value)
    b_value_elem = etree.SubElement(
        truncatd_gutenberg_rich_elem, nrml_xml.B_VALUE)
    b_value_elem.text = \
        str(truncated_gutenberg_richter.b_value)

    min_magnitude_elem = etree.SubElement(
        truncatd_gutenberg_rich_elem, nrml_xml.MIN_MAGNITUDE)
    min_magnitude_elem.text = \
        str(truncated_gutenberg_richter.min_magnitude)

    max_magnitude_elem = etree.SubElement(
        truncatd_gutenberg_rich_elem, nrml_xml.MAX_MAGNITUDE)
    max_magnitude_elem.text = \
        str(truncated_gutenberg_richter.max_magnitude)

def _write_rupture_depth_distrib(container_elem,
    rupture_depth_dist):
    """
    Attach a rupture depth distribution element
    to the element container.
    :param container_elem: element which contains rupture depth
     distribution
    :type container_elem: lxml.etree._Element
    :param rupture_depth_dist: rupture depth distribution object
    :type rupture_depth_dist: py:class::RuptureDepthDistrib
    """

    rupture_depth_distrib_elem = etree.SubElement(
        container_elem, nrml_xml.RUPTURE_DEPTH_DISTRIB)

    magnitude_elem = etree.SubElement(
        rupture_depth_distrib_elem, nrml_xml.MAGNITUDE)
    magnitude_elem.attrib[nrml_xml.TYPE] = \
        rupture_depth_dist.magnitude.type_mag
    magnitude_elem.text = ' '.join(
        (str(value) for value in
            rupture_depth_dist.magnitude.values))

    depth_elem = etree.SubElement(
        rupture_depth_distrib_elem, nrml_xml.DEPTH)
    depth_elem.text = ' '.join(
        (str(value) for value in
            rupture_depth_dist.depth))
