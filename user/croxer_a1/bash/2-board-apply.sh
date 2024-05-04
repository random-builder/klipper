#!/usr/bin/env bash

#
# update firmware on remote host
#

set -e

this_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

source $this_dir/arkon.sh

klipper_service enable

echo "### board copy"
scp $this_dir/board*.*  $ssh_user_url:$print3d_this_dir

octoprint_connection disconnect
klipper_service stop
ssh $ssh_user_url "rm -f $print3d_logs_file"

echo "### board setup"
ssh $ssh_user_url "cd $print3d_this_dir; MENU_WORD='' ./board.sh"

klipper_service start
sleep 3
octoprint_connection connect

echo "### operation complete"
