#===----------------------------------------------------------------------===##
#
# Part of the LLVM Project, under the Apache License v2.0 with LLVM Exceptions.
# See https://llvm.org/LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
#
#===----------------------------------------------------------------------===##
import os
import sys

from libcxx.test.config import Configuration as LibcxxConfiguration


class Configuration(LibcxxConfiguration):
    # pylint: disable=redefined-outer-name
    def __init__(self, lit_config, config):
        super(Configuration, self).__init__(lit_config, config)
        self.libunwind_src_root = None
        self.libunwind_obj_root = None
        self.abi_library_root = None
        self.libcxx_src_root = None

    def configure_src_root(self):
        self.libunwind_src_root = (self.get_lit_conf('libunwind_src_root')
            or os.path.dirname(self.config.test_source_root))
        self.libcxx_src_root = (self.get_lit_conf('libcxx_src_root')
            or os.path.join(self.libunwind_src_root, '..', 'libcxx'))

    def configure_obj_root(self):
        self.libunwind_obj_root = self.get_lit_conf('libunwind_obj_root')
        super(Configuration, self).configure_obj_root()

    def has_cpp_feature(self, feature, required_value):
        return int(self.cxx.dumpMacros().get('__cpp_' + feature, 0)) >= required_value

    def configure_features(self):
        super(Configuration, self).configure_features()
        if self.get_lit_bool('arm_ehabi', False):
            self.config.available_features.add('libunwind-arm-ehabi')

    def configure_compile_flags(self):
        self.cxx.compile_flags += ['-DLIBUNWIND_NO_TIMER']
        # Stack unwinding tests need unwinding tables and these are not
        # generated by default on all Targets.
        self.cxx.compile_flags += ['-funwind-tables']
        # Make symbols available in the tests.
        if 'linux' in self.config.target_triple:
            self.cxx.link_flags += ['-Wl,--export-dynamic']
        if not self.get_lit_bool('enable_threads', True):
            self.cxx.compile_flags += ['-D_LIBUNWIND_HAS_NO_THREADS']
            self.config.available_features.add('libunwind-no-threads')
        super(Configuration, self).configure_compile_flags()

    def configure_compile_flags_header_includes(self):
        self.configure_config_site_header()

        libunwind_headers = self.get_lit_conf(
            'libunwind_headers',
            os.path.join(self.libunwind_src_root, 'include'))
        if not os.path.isdir(libunwind_headers):
            self.lit_config.fatal("libunwind_headers='%s' is not a directory."
                                  % libunwind_headers)
        self.cxx.compile_flags += ['-I' + libunwind_headers]

    def configure_link_flags_cxx_library(self):
        # libunwind tests should not link with libc++
        pass

    def configure_link_flags_abi_library(self):
        # libunwind tests should not link with libc++abi
        pass
