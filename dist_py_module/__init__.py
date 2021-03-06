# -*- coding: UTF-8 -*-

'''
 Module
     __init__.py
 Copyright
     Copyright (C) 2018 Vladimir Roncevic <elektron.ronca@gmail.com>
     dist_py_module is free software: you can redistribute it and/or modify it
     under the terms of the GNU General Public License as published by the
     Free Software Foundation, either version 3 of the License, or
     (at your option) any later version.
     dist_py_module is distributed in the hope that it will be useful, but
     WITHOUT ANY WARRANTY; without even the implied warranty of
     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
     See the GNU General Public License for more details.
     You should have received a copy of the GNU General Public License along
     with this program. If not, see <http://www.gnu.org/licenses/>.
 Info
     Define class DistPyModule with attribute(s) and method(s).
     Load a base info, create an CLI interface and run operation(s).
'''

import sys
from os import getcwd

try:
    from pathlib import Path
    from dist_py_module.setup import GenSetup
    from ats_utilities.cli.cfg_cli import CfgCLI
    from ats_utilities.console_io.error import error_message
    from ats_utilities.console_io.verbose import verbose_message
    from ats_utilities.console_io.success import success_message
except ImportError as error_message:
    MESSAGE = '\n{0}\n{1}\n'.format(__file__, error_message)
    sys.exit(MESSAGE)  # Force close python ATS ##############################

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright 2018, Free software to use and distributed it.'
__credits__ = ['Vladimir Roncevic']
__license__ = 'GNU General Public License (GPL)'
__version__ = '1.5.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DistPyModule(CfgCLI):
    '''
        Define class DistPyModule with attribute(s) and method(s).
        Load a base info, create an CLI interface and run operation(s).
        It defines:

            :attributes:
                | __slots__ - Setting class slots.
                | VERBOSE - Console text indicator for current process-phase.
                | __CONFIG - Tool info file path.
                | __OPS -  List of tool options.
            :methods:
                | __init__ - Initial constructor.
                | process - Process and generate module setup.py.
    '''

    __slots__ = ('VERBOSE', '__CONFIG', '__OPS')
    VERBOSE = 'DIST_PY_MODULE'
    __CONFIG = '/conf/dist_py_module.cfg'
    __OPS = ['-g', '--gen', '-v']

    def __init__(self, verbose=False):
        '''
            Initial constructor.

            :param verbose: Enable/disable verbose option.
            :type verbose: <bool>
            :exceptions: None
        '''
        verbose_message(DistPyModule.VERBOSE, verbose, 'init tool info')
        current_dir = Path(__file__).resolve().parent
        base_info = '{0}{1}'.format(current_dir, DistPyModule.__CONFIG)
        CfgCLI.__init__(self, base_info, verbose=verbose)
        if self.tool_operational:
            self.add_new_option(
                DistPyModule.__OPS[0], DistPyModule.__OPS[1], dest='pkg',
                help='generate module setup.py'
            )
            self.add_new_option(
                DistPyModule.__OPS[2], action='store_true', default=False,
                help='activate verbose mode for generation'
            )

    def process(self, verbose=False):
        '''
            Process and run operation.

            :param verbose: Enable/disable verbose option.
            :type verbose: <bool>
            :return: True (success) | False.
            :rtype: <bool>
            :exceptions: None
        '''
        status = False
        if self.tool_operational:
            num_of_args_sys = len(sys.argv)
            if num_of_args_sys >= 1:
                operation = sys.argv[1]
                if operation not in DistPyModule.__OPS:
                    sys.argv = []
                    sys.argv.append('-h')
            else:
                sys.argv.append('-h')
            opts, args = self.parse_args(sys.argv)
            num_of_args, setup_exists = len(args), Path(
                '{0}/{1}'.format(getcwd(), 'setup.py')
            ).exists()
            if not setup_exists:
                if num_of_args >= 1 and bool(opts.pkg):
                    print(
                        '{0} {1} [{2}]'.format(
                            '[{0}]'.format(DistPyModule.VERBOSE.lower()),
                            'generating setup.py for package', opts.pkg
                        )
                    )
                    generator = GenSetup(verbose=opts.v or verbose)
                    status = generator.gen_setup(
                        '{0}'.format(opts.pkg), verbose=opts.v or verbose
                    )
                    if status:
                        success_message(DistPyModule.VERBOSE, 'done\n')
                    else:
                        error_message(
                            DistPyModule.VERBOSE, 'generation failed'
                        )
                else:
                    error_message(
                        DistPyModule.VERBOSE, 'provide package name'
                    )
            else:
                error_message(
                    DistPyModule.VERBOSE, 'setup.py already exist'
                )
        else:
            error_message(
                DistPyModule.VERBOSE, 'tool is not operational'
            )
        return True if status else False
