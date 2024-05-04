#!/usr/bin/env bash

#
# update printer config on remote host
#

set -e

this_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

source $this_dir/arkon.sh

echo "### config copy"
scp $this_dir/printer*.cfg  $ssh_user_url:$print3d_this_dir

octoprint_connection disconnect
klipper_service stop
sleep 1
ssh $ssh_user_url "rm -f $print3d_logs_file"

klipper_service start

#while true ; do
sleep 3
echo "### device init"
ssh $ssh_user_url "echo FIRMWARE_RESTART > $print3d_device_tty"
#done

octoprint_connection connect

echo "### operation complete"
