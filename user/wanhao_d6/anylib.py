#
#
#

import os
import time
from dataclasses import dataclass

this_dir = os.path.dirname(__file__)
print(f"{this_dir=}")

make_host = "make_print@make1"


def invoke_xterm(plain_command:str) -> None:
    xterm_command = f"xterm -fa Monospace -fs 16 -e {plain_command}"
    assert os.system(xterm_command) == 0


def invoke_ssh_exec(command:str) -> None:
    assert os.system(f"ssh '{make_host}' '{command}'") == 0


def invoke_ssh_copy(source:str, target:str) -> None:
    assert os.system(f"scp '{source}' '{target}'") == 0


@dataclass
class KlipperBean:

    source_dir:str
    profile_name:str
    flash_device:str

    @property
    def local_repo_root(self) -> str:
        return os.popen("git rev-parse --show-toplevel").readline().strip()

    @property
    def klipper_unit(self) -> str:
        return f"make_klipper-{self.profile_name}.service"

    @property
    def klipper_data(self) -> str:
        return f"/home/make_print/{self.profile_name}/klip/data"

    @property
    def klipper_repo(self) -> str:
        return f"/home/make_print/{self.profile_name}/klip/repo"

    @property
    def source_config(self) -> str:
        return f"{self.source_dir}/config.cfg"

    @property
    def target_config(self) -> str:
        return f"{self.klipper_repo}/user/{self.profile_name}/config.cfg"

    @property
    def source_printer(self) -> str:
        return  f"{self.source_dir}/printer.cfg"

    @property
    def target_printer(self) -> str:
        return f"{self.klipper_repo}/user/{self.profile_name}/printer.cfg"

    @property
    def source_service_log(self) -> str:
        return f"{self.source_dir}/service.log"

    @property
    def target_service_log(self) -> str:
        return f"{self.klipper_data}/service.log"

    def local_build_clean(self) -> None:
        print_report("local_build_clean")
        os.chdir(self.local_repo_root)
        invoke_plain(f"make KCONFIG_CONFIG={self.source_config} distclean")

    def local_build_config(self) -> None:
        print_report("local_build_config")
        os.chdir(self.local_repo_root)
        invoke_xterm(f"make KCONFIG_CONFIG={self.source_config} menuconfig")

    def local_build_make(self) -> None:
        print_report("local_build_make")
        os.chdir(self.local_repo_root)
        invoke_plain(f"make KCONFIG_CONFIG={self.source_config}")

    def remote_unit_restart(self) -> None:
        print_report("remote_unit_restart")
        invoke_ssh_exec(f"sudo systemctl stop {self.klipper_unit}")
        invoke_ssh_exec(f"rm -rf {self.target_service_log}")
        invoke_ssh_exec(f"sudo systemctl start {self.klipper_unit}")

    def remote_unit_start(self) -> None:
        print_report("remote_unit_start")
        invoke_ssh_exec(f"sudo systemctl start {self.klipper_unit}")

    def remote_unit_stop(self) -> None:
        print_report("remote_unit_stop")
        invoke_ssh_exec(f"sudo systemctl stop {self.klipper_unit}")

    def remote_repo_update(self) -> None:
        print_report("remote_repo_update")
        invoke_ssh_exec(f"cd {self.klipper_repo} ; git reset --hard")
        invoke_ssh_exec(f"cd {self.klipper_repo} ; git clean -f -d")
        invoke_ssh_exec(f"cd {self.klipper_repo} ; git pull")

    def remote_build_clean(self) -> None:
        print_report("remote_build_clean")
        invoke_ssh_exec(f"cd {self.klipper_repo} ; make KCONFIG_CONFIG={self.target_config} distclean")

    def publish_build_config(self) -> None:
        print_report("publish publish_build_config")
        invoke_ssh_copy(f"{self.source_config}", f"{make_host}:{self.target_config}")

    def publish_printer_config(self) -> None:
        print_report("publish_printer_config")
        invoke_ssh_exec(f"dirname {self.target_printer} | xargs mkdir -p")
        invoke_ssh_copy(f"{self.source_printer}", f"{make_host}:{self.target_printer}")

    def remote_build_make(self) -> None:
        print_report("remote_build_make")
        invoke_ssh_exec(f"cd {self.klipper_repo} ; make KCONFIG_CONFIG={self.target_config}")

    def remote_build_flash(self) -> None:
        print_report("remote_build_flash")
        invoke_ssh_exec(f"cd {self.klipper_repo} ; make flash KCONFIG_CONFIG={self.target_config} FLASH_DEVICE={self.flash_device}")

    def perform_local_config_verify(self) -> None:
        self.local_build_clean()
        self.local_build_config()
        self.local_build_make()

    def perform_remote_build_update(self) -> None:
        self.remote_unit_stop()
        self.remote_repo_update()
        self.remote_build_clean()
        self.publish_build_config()
        self.remote_build_make()
        self.remote_build_flash()
        self.remote_unit_start()

    def perform_remote_printer_update(self) -> None:
        self.publish_printer_config()
        self.remote_unit_restart()
        self.produce_remote_printer_status()

    def produce_remote_printer_status(self) -> None:
        print_report("produce_remote_printer_status")
        time.sleep(1.5)
        invoke_ssh_copy(f"{make_host}:{self.target_service_log}", f"{self.source_service_log}")
        invoke_plain(f"cat {self.source_service_log} | grep 'Loaded MCU'")


def print_report(message:str) -> None:
    print(f"### {message} ###".upper())


def invoke_plain(command:str) -> None:
    assert os.system(command) == 0


klipper_bean = KlipperBean(
    this_dir,
    "wanhao_d6",
    "/dev/serial/by-id/usb-Klipper_lpc1768_16100006262006AF566E6E58C32000F5-if00",
)

#
#
#
