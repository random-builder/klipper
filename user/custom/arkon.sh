#!/usr/bin/env bash

#
# setup config for "make menuconfig"
#

set -e

export TERM=xterm

this_dir=$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )
base_dir=$( cd $this_dir/../.. && pwd )

echo "### base_dir=$base_dir"
echo "### this_dir=$this_dir"

base_config=$base_dir/.config
this_config=$this_dir/config.cfg

cd $base_dir

echo "### remove build and config"
make distclean

echo "### setup custom build config"
ln -s $this_config $base_config
 
echo "### invoke firmware config editor"
make menuconfig

echo "### produce custom board firmware image"
make

#
#
#
