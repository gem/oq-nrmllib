# -*- coding: utf-8 -*-
# Copyright (c) 2010-2011, GEM Foundation.
#
# Nrmllib is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License version 3
# only, as published by the Free Software Foundation.
#
# Nrmllib is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License version 3 for more details
# (a copy is included in the LICENSE file that accompanied this code).
#
# You should have received a copy of the GNU Lesser General Public License
# version 3 along with Nrmllib.  If not, see
# <http://www.gnu.org/licenses/lgpl-3.0.txt> for a copy of the LGPLv3 License.

"""
This is our basic test running framework.

Usage Examples:
# to run all the tests
python run_tests.py

"""

import os
import sys
import nose

if __name__ == '__main__':
    sys.path.append("%s/tests" % os.path.abspath(os.path.curdir))
    args = sys.argv
    args.remove('run_tests.py')
    args = ['nosetests'] + args
    nose.run(defaultTest='tests', argv=args)
