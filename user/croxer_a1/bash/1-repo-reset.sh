#!/usr/bin/env bash

#
# update firmware on remote host
#

set -e

this_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

source $this_dir/arkon.sh

echo "### repo reset"
ssh $ssh_user_url "cd $print3d_repo_dir; git reset --hard"

echo "### repo update"
ssh $ssh_user_url "cd $print3d_repo_dir; git pull"
