#!/usr/bin/env bash

#
#
#

readonly this_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
readonly base_dir="$( cd "$this_dir/../.." && pwd)"

echo "### base_dir=$base_dir"
echo "### this_dir=$this_dir"

readonly logger_file=$this_dir/printer-verify.log
readonly socket_file=$this_dir/printer-verify.tty

rm $logger_file $socket_file 

/usr/bin/python \
    $base_dir/klippy/klippy.py \
    $this_dir/printer.cfg \
    --logfile    $logger_file \
    --input-tty  $socket_file \
