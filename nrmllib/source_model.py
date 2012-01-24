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
The purpose of this module is to provide value objects
representing the different elements inside the
NRML data format.
"""

from collections    import namedtuple


POINT = namedtuple('Point', 'lon, lat')

AREA_BOUNDARY = namedtuple('AreaBoundary', 'srs_name, pos_list')

TRUNCATED_GUTEN_RICHTER = namedtuple(
    'TruncatedGutenRichter',
    'a_value, b_value, min_magnitude, max_magnitude, type_tgr')

RUPTURE_RATE_MODEL = namedtuple(
    'RuptureRateModel', 'truncated_gutenberg_richter, strike, dip, rake')

MAGNITUDE = namedtuple('Magnitude', 'type_mag, values')

RUPTURE_DEPTH_DISTRIB = namedtuple(
    'RuptureDepthDistrib', 'magnitude, depth')


class AreaSource(object):
    """
    AreaSource value object
    """

    def __init__(self):
        self.nrml_id = None
        self.source_model_id = None
        self.area_source_id = None
        self.name = None
        self.tectonic_region = None
        self.area_boundary = None
        self.rupture_rate_model = None
        self.rupture_depth_dist = None
        self.hypocentral_depth = None

    def __str__(self):

        area_source = ['Area Source Object',
                    'nrml id: %s' % (self.nrml_id),
                    'source model id: %s' % (self.source_model_id),
                    'area source id: %s' % (self.area_source_id),
                    'name: %s' % (self.name),
                    'tectonic region: %s' % (self.tectonic_region),
                    '%s' % self.area_boundary.__str__(),
                    '%s' % self.rupture_rate_model.__str__(),
                    '%s' % self.rupture_depth_dist.__str__(),
                    'hypocentral depth: %s' % self.hypocentral_depth]

        return  '\n'.join(area_source)

    def __eq__(self, oth):

        return  (self.nrml_id == oth.nrml_id
                and self.source_model_id == oth.source_model_id
                and self.area_source_id == oth.area_source_id
                and self.name == oth.name
                and self.tectonic_region == oth.tectonic_region
                and self.area_boundary == oth.area_boundary
                and self.rupture_rate_model == oth.rupture_rate_model
                and self.rupture_depth_dist == oth.rupture_depth_dist
                and self.hypocentral_depth == oth.hypocentral_depth)

    def __ne__(self, other):
        return not self.__eq__(other)
