#
#
#

import os

base_dir = os.popen("git rev-parse --show-toplevel").readline().strip()
this_dir = os.path.dirname(__file__)
print(f"{base_dir=}")
print(f"{this_dir=}")

make_host = "make_print@make1"

klipper_unit = "make_klipper-wanhao_d6.service"
klipper_data = "/home/make_print/wanhao_d6/klip/data"
klipper_repo = "/home/make_print/wanhao_d6/klip/repo"

this_config = f"{this_dir}/config.cfg"

source_config = f"{base_dir}/.config"
target_config = f"{klipper_repo}/.config"

source_printer = f"{this_dir}/printer.cfg"
target_printer = f"{klipper_repo}/user/custom/printer.cfg"

source_service_log = f"{this_dir}/service.log"
target_service_log = f"{klipper_data}/service.log"


def print_report(message:str) -> None:
    print(f"### {message} ###".upper())


def invoke_plain(command:str) -> None:
    assert os.system(command) == 0


def invoke_xterm(plain_command:str) -> None:
    xterm_command = f"xterm -fa Monospace -fs 16 -e {plain_command}"
    assert os.system(xterm_command) == 0


def invoke_ssh_exec(command:str) -> None:
    assert os.system(f"ssh '{make_host}' '{command}'") == 0


def invoke_ssh_copy(source:str, target:str) -> None:
    assert os.system(f"scp '{source}' '{target}'") == 0

#
#
#
