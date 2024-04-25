#!/usr/bin/env python

#
# setup "make menuconfig"
#

from anylib import *

os.chdir(base_dir)

print_report("remove build and config")
invoke_plain(f"make distclean")

print_report("setup custom build config")
invoke_plain(f"ln -v -s {this_config} {source_config}")

print_report("invoke firmware config editor")
invoke_xterm(f"make menuconfig")

print_report("produce custom firmware image")
invoke_plain(f"make")

#
#
#
