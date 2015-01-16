# Copyright (c) 2010-2014, GEM Foundation.
#
# NRML is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# NRML is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with NRML.  If not, see <http://www.gnu.org/licenses/>.

"""
NRML base path
"""

import os
from lxml import etree

__version__ = "0.4.6"

NAMESPACE = 'http://openquake.org/xmlns/nrml/0.4'
GML_NAMESPACE = 'http://www.opengis.net/gml'

PARSE_NS_MAP = {'nrml': NAMESPACE, 'gml': GML_NAMESPACE}
#: Default namespace is nrml, so we can be implicit about nrml elements we
#: write
SERIALIZE_NS_MAP = {None: NAMESPACE, 'gml': GML_NAMESPACE}

_NRML_SCHEMA_FILE = 'nrml.xsd'

_NRML_SCHEMA = None  # defined in assert_valid


class InvalidFile(Exception):
    pass


def nrml_schema_file():
    """
    Returns the absolute path to the NRML schema file
    """
    return os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        'schema', _NRML_SCHEMA_FILE)

COMPATPARSER = etree.ETCompatXMLParser()


def assert_valid(source, parser=COMPATPARSER):
    """
    Raises a `lxml.etree.DocumentInvalid` error for invalid files.
    NB: it works by keeping the whole tree in memory.

    :param source: a filename or a file-like object.
    """
    global _NRML_SCHEMA
    if isinstance(source, basestring):
        fname = source
        if not os.path.exists(fname):
            raise IOError('[Errno 2] No such file or directory: %r' % fname)
    else:
        fname = getattr(source, 'name', '<%s>' % source.__class__.__name__)
    if _NRML_SCHEMA is None:  # the nrml schema is parsed only once
        _NRML_SCHEMA = etree.XMLSchema(etree.parse(nrml_schema_file()))
    try:
        parsed = etree.parse(source, parser)
        _NRML_SCHEMA.assertValid(parsed)
    except Exception as e:
        raise InvalidFile('%s:%s' % (fname, e))
    return parsed


class NRMLFile(object):
    """
    Context-managed output object which accepts either a path or a file-like
    object.

    Behaves like a file.
    """

    def __init__(self, dest, mode='r'):
        self._dest = dest
        self._mode = mode
        self._file = None

    def __enter__(self):
        if isinstance(self._dest, (basestring, buffer)):
            self._file = open(self._dest, self._mode)
        else:
            # assume it is a file-like; don't change anything
            self._file = self._dest
        return self._file

    def __exit__(self, *args):
        self._file.close()


def iterparse_tree(source, events=('start', 'end')):
    schema = etree.XMLSchema(etree.parse(nrml_schema_file()))

    tree = etree.iterparse(source, events=events, schema=schema)
    return tree
