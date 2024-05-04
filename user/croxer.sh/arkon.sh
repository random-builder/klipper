#!/usr/bin/env bash

#
# global config
#

readonly print3d_unit="1"
readonly print3d_user="print3d"

readonly print3d_klip_dir="$print3d_unit/klip"

readonly print3d_data_dir="$print3d_klip_dir/data"
readonly print3d_logs_file="$print3d_data_dir/service.log"
readonly print3d_device_tty="$print3d_data_dir/printer.tty"

readonly print3d_repo_dir="$print3d_klip_dir/repo"
readonly print3d_this_dir="$print3d_repo_dir/user/croxer"

readonly print3d_service="klipper@$print3d_unit.service"

readonly octoprint_host="octo1"
readonly octoprint_port="500$print3d_unit"
readonly octoprint_url="http://$octoprint_host:$octoprint_port"

readonly ssh_root_url="root@$octoprint_host"
readonly ssh_user_url="$print3d_user@$octoprint_host"

klipper_service() {
    local command="$1"
    echo "### service $command : $print3d_service"
    ssh $ssh_root_url "systemctl $command $print3d_service"
}

octoprint_connection() {
    local command="$1"
    echo "### octoprint $command : $octoprint_url"
    curl \
    --silent \
    --request POST \
    --header "X-Api-Key: AD1D0068CFB74AC9BC447D23B8FC7656" \
    --header "Accept: application/json" \
    --header "Content-Type: application/json" \
    --data '{ "command":"'$command'" }' \
    $octoprint_url/api/connection
}
